import pathlib
from functools import reduce

from lxml import etree
from typing import Iterable, Optional, Tuple

from .note import Note
from .part import Part
from .rest import Rest
from .measure import Measure
from .beat import Beat
from .chord import Chord

import lejaren.log.log as logger
log = logger.get_logger()

from .score_helper_funcs import _convert_score_parts_to_xml, _from_etree
from ._parse_parts import _parse_parts
from ._pad_with_empty_measures import _pad_with_empty_measures

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
                self._parts = _parse_parts(parts)
            elif len(parts) == reduce(lambda acc, item: acc + 1 if isinstance(item, Part) else acc, parts, 0) and len(parts) > 0:
                self._parts = _parse_parts(parts)
            else:
                warnstr = f"Some parts wrong... count:{len(parts)} and part: {reduce(lambda acc, item: acc + 1 if isinstance(item, Part) else acc, parts, 0)}"
                log.warning(warnstr)
                raise ValueError(warnstr)
            self._measure_count = _pad_with_empty_measures(self._parts)
        elif isinstance(parts, etree.ElementTree):
            log.debug(f"Creating a lejaren score from a etree, is: {parts}")
            self._parts = _from_etree(parts)
            if len(self._parts) < 0:
                warnstr = "No parts exist, Aborting."
                log.warning(warnstr)
                raise ValueError(warnstr)
            self._measure_count = len(self._parts)
        elif isinstance(parts, pathlib.Path):
            log.debug(f"Creating a lejaren score from a file, file is: {parts}")
            temp_tree = etree.parse(parts)
            temp_root = temp_tree.getroot()
            self._parts = _from_etree(temp_tree)
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
                self._parts = _from_etree(temp_tree)
        else:
            warnstr = f"Parts must be Lejaren Parts, ETree or Path, is {type(parts)}"
            log.warning(warnstr)
            raise TypeError(warnstr)



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


    