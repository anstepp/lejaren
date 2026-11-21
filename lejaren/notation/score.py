import pathlib
from functools import reduce

from lxml import etree
from typing import Iterable, Optional

from .part import Part

import lejaren.log.log as logger
log = logger.get_logger()

from ._convert_parts_to_xml import _convert_score_parts_to_xml
from ._from_etree import _from_etree
from ._write_xml_to_file import _write_xml_to_file
from ._parse_parts import _parse_parts
from ._pad_with_empty_measures import _pad_with_empty_measures
from ._join_ties import _join_ties

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
        _write_xml_to_file(output_filepath, xml_score)


    