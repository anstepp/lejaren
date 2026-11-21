import pathlib
from functools import reduce

from lxml import etree
from lxml.etree import _Element
from typing import Iterable, Optional, Tuple

from .note import Note
from .part import Part
from .rest import Rest
from .measure import Measure
from .beat import Beat
from .chord import Chord
import lejaren.log.log as logger

from lejaren._constants import ARTICULATIONS, DIATONIC

log = logger.get_logger()

EMPTY_MEASURE_FACTOR = 1

from .score_helper_funcs import _convert_score_parts_to_xml

class Score:
    """Generates a MusicXML score from a list of parts (NoteLists) and outputs score to file"""

    def __init__(
        self,
        parts: Iterable[Iterable[Part]] | etree,
        title: Optional[str] = None,
        composer: Optional[str] = None,
    ):


        log.info(f"Making a part, parts is... {parts}")
    
        self.title = title
        self.composer = composer

        #FIXME: Add really nice testing for this so we know it acutally works right
        if isinstance(parts, list) or isinstance(parts, Part):
            if isinstance(parts, Part):
                log.debug(f"Creating a lejaren score from a parts, parts is: {parts}")
                self._parts = self._parse_parts(parts)
            elif len(parts) == reduce(lambda acc, item: acc + 1 if isinstance(item, Part) else acc, parts, 0) and len(parts) > 0:
                self._parts = self._parse_parts(parts)
            else:
                warnstr = f"Some parts wrong... count:{len(parts)} and part: {reduce(lambda acc, item: acc + 1 if isinstance(item, Part) else acc, parts, 0)}"
                log.warning(warnstr)
                raise ValueError(warnstr)
            self._measure_count = self._pad_with_empty_measures()
        elif isinstance(parts, etree.ElementTree):
            log.debug(f"Creating a lejaren score from a etree, is: {parts}")
            self._parts = self._from_etree(parts)
            if len(self._parts) < 0:
                warnstr = "No parts exist, Aborting."
                log.warning(warnstr)
                raise ValueError(warnstr)
            self._measure_count = len(self._parts)
        elif isinstance(parts, pathlib.Path):
            log.debug(f"Creating a lejaren score from a file, file is: {parts}")
            temp_tree = etree.parse(parts)
            temp_root = temp_tree.getroot()
            self._parts = self._from_etree(temp_tree)
        elif isinstance(parts, str):
            if not pathlib.Path(parts).exists():
                warnstr = f"Path was string; unable to load file as it does not exist, path was: {parts}"
                log.warning(warnstr)
                raise ValueError(warnstr)
            else:
                log.debug(f"Creating a lejaren score from a file, file is: {parts}")
                parts_path = pathlib.Path(parts)
                temp_tree = etree.parse(parts_path)
                temp_root = temp_tree.getroot()
                self._parts = self._from_etree(temp_tree)
        else:
            warnstr = f"Parts must be Lejaren Parts, ETree or Path, is {type(parts)}"
            log.warning(warnstr)
            raise TypeError(warnstr)
            
        

    def _from_etree(self, parts, time_signatures=[(4,4)]):
        #FIXME: Get away from findall...?
        part_list = []
        root = parts.getroot()
        divisions = 1.0
        for part in root.iterchildren('part'):
            part_note_list = []
            for measure in part.iterchildren('measure'):
                log.critical(repr(measure.findtext('attributes/divisions', default='')))

                if not measure.findtext('attributes/divisions', default='').strip():
                    if measure.get("number") == 1:
                        log.warning("First measure has no divisions; setting to 1.0")
                    else:
                        log.info(f"No division on imported measure {measure.get("number")} was {measure.findtext('attributes/divisions')}, using previous divisons: {divisions}")
                else:
                    new_div = float(measure.findtext('attributes/divisions', default=divisions))
                    log.info(f"New divisions set in measure: {measure.get("number")}, old divisions {divisions}, new: {new_div}")
                    divisions = new_div
                if sum(1 for _ in measure.iterchildren(tag='note')) < 0:
                    warnstr = f"No notes in this measure, count is {sum(1 for _ in measure.iterchildren(tag='note'))}"
                    log.warning(warnstr)
                    raise ValueError(warnstr)
                else:
                    for note in measure.iterchildren('note'):
                        if self._note_check(note):
                            # FIXME: Save minimum necessary info
                            # Try to stick with XPath for now...
                            if not isinstance(note.findall('.//duration'), list):
                                warnstr = f"Note durations not list is: {type(note.findall('.//duration'))}"
                                log.warning(warnstr)
                                raise TypeError(warnstr)
                            else:
                                dur = float(note.findall('.//duration')[0].text)
                                dur /= divisions
                            if not isinstance(note.findall('.//step'), list):
                                warnstr = f"Note step not list is: {type(note.findall('.//step'))}"
                                log.warning(warnstr)
                                raise TypeError(warnstr)
                            elif (len(note.findall('.//step')) < 1):
                                warnstr = f"Note step not list has no values: {len(note.findall('.//step'))}"
                                log.warning(warnstr)
                                raise ValueError(warnstr)
                            else:
                                log.info(note.findall('.//step')[0].text)
                                step = int(DIATONIC[note.findall('.//step')[0].text])
                            if not isinstance(note.findall('.//octave'), list):
                                raise TypeError(f"Note step not list is: {type(note.findall('.//octave'))}")
                            else:
                                octave = note.findall('.//octave')[0].text
                            if not (note.findtext('.//alter', default=None)):
                                log.info(f"No accidental text for alter value... setting to 0... was: {note.findtext('.//alter', default=None)}")
                                alter = 0
                                step += alter
                            else:
                                alter = float(note.findtext('.//alter', default=0))
                                step += alter
                            part_note_list.append(Note(float(dur), int(octave), step))
                            #join notes
                            #part_note_list = self._join_ties(part_note_list)
            part_list.append(Part(part_note_list, time_signatures))
        parsed_parts = self._parse_parts(part_list)
        return parsed_parts

    def _parse_parts(self, parts) -> Iterable[Part]:

        parsed_parts = []

        # parts is a single Part object.
        if isinstance(parts, Part):
            parsed_parts = [{"staff_count": 1, "staves": [parts]}]

        # parts is a list.
        elif isinstance(parts, list):
            parsed_parts = []

            for p in parts:
                if isinstance(p, list):
                    parsed_parts.append({"staff_count": len(p), "staves": p})
                else:
                    parsed_parts.append({"staff_count": 1, "staves": [p]})

        else:
            warnstr = "Invalid parts argument supplied to Score."
            log.warning(warnstr)
            raise TypeError(warnstr)

        return parsed_parts

    def _pad_with_empty_measures(self) -> int:
        """Returns score measure length (ie. max number of measures)"""

        max_len = 0

        # figure out which staff is the longest (largest number of measures)
        for part in self._parts:
            for staff in part["staves"]:
                if len(staff.measures) > max_len:
                    max_len = len(staff.measures)
                    longest_staff = staff

        for part in self._parts:
            for staff in part["staves"]:
                if len(staff.measures) < max_len:
                    for idx in range(len(staff.measures), max_len):
                        ts = longest_staff.measures[idx].time_signature
                        measure_to_append = Measure(ts, EMPTY_MEASURE_FACTOR)

                        full_rest = ts[0]
                        empty_beat = Beat(ts[0])
                        empty_beat.add_note(Rest(full_rest))
                        measure_to_append.add_beat(empty_beat)
                        staff.measures.append(measure_to_append)

        return max_len

    def convert_to_xml(self, output_filepath: str) -> None:
        """Entrypoint to Score class
        * converts self.parts (list of NoteLists) to a MusicXML tree
        * writes MusicXML tree to .xml file
        """
        xml_score = _convert_score_parts_to_xml(self)
        self._write_xml_to_file(output_filepath, xml_score)

    def _join_ties(self, note_list: list) -> list:
        tie_attr_list = ("tie_start", "tie_end", "tie_continue")
        for idx, note in enumerate(note_list):
            if any(hasattr(note, attr) for attr in tie_attr_list):
                #Verify adjacent notes tied
                if "tie_start":
                    if hasattr(note[idx+1], "tie_continue"):
                        pass
                    if hasattr(note[idx+1], "tie_end"):
                        pass
                if "tie_end":
                    # This probably shouldn't happen! Test for it.
                    log.warning("Check Tie End in Score _join_ties")
                    pass
                if "tie_continue":
                    # Might not be supposed to happen... test for it.
                    log.warning("Check Tie Continue in _join_ties")
                    pass

    def _write_xml_to_file(
        self, output_filepath: str, xml_score: etree.ElementTree
    ) -> None:
        """Write MusicXML tree to output file"""
        output_filepath = pathlib.Path(output_filepath)
        xml_score.write(
            str(output_filepath),
            pretty_print=True,
            encoding="UTF-8",
            xml_declaration=True,
        )


    def _note_check(self, note: _Element) -> bool:
        # Use fall-through set to true; probably could be changed

        note_ok = False
        if (note.findall('.//duration') and note.findall('.//step') and note.findall('.//octave')):
            note_ok = True
        elif (len(note.findall('.//duration')) > 0 and len(note.findall('.//step')) > 0 and len(note.findall('.//octave'))) > 0:
            note_ok = True
        else:
            pass

        return note_ok