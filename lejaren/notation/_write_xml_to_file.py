from __future__ import annotations

from typing import TYPE_CHECKING

from pathlib import Path
from lxml.etree import ElementTree

# avoid circular import
if TYPE_CHECKING:
    from .score import Score

def _write_xml_to_file(
    output_filepath: str, 
    xml_score: ElementTree
) -> None:
    """Write MusicXML tree to output file"""
    output_filepath = Path(output_filepath)
    xml_score.write(
        str(output_filepath),
        pretty_print=True,
        encoding="UTF-8",
        xml_declaration=True,
    )