from lxml import etree

from .note import Note
from .part import Part
from lejaren._constants import DIATONIC

from ._note_check import _note_check
from ._parse_parts import _parse_parts

import lejaren.log.log as logger
log = logger.get_logger()

def _from_etree(parts, time_signatures=[(4,4)]):
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
                        if _note_check(note):
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
        parsed_parts = _parse_parts(part_list)
        return parsed_parts