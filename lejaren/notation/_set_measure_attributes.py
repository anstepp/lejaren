from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from lxml import etree

from .note import Note
from .part import Part
from .rest import Rest
from .measure import Measure
from .beat import Beat
from .chord import Chord
# avoid circular import
if TYPE_CHECKING:
    from .score import Score
    
def _set_measure_attributes(
    xml_measure: etree.SubElement,
    time_sig: Tuple[int, int],
    divisions: int,
    staff_count: int,
) -> etree.SubElement:

    # attributes on the measure
    #   -> divisions, key, time, clef

    xml_part_attributes = etree.SubElement(xml_measure, "attributes")

    xml_part_divisions = etree.SubElement(xml_part_attributes, "divisions")
    xml_part_divisions.text = str(divisions)

    xml_part_key = etree.SubElement(xml_part_attributes, "key")
    xml_part_fifths = etree.SubElement(xml_part_key, "fifths")
    xml_part_fifths.text = "0"
    xml_part_mode = etree.SubElement(xml_part_key, "mode")
    xml_part_mode.text = "none"

    xml_part_time = etree.SubElement(xml_part_attributes, "time")
    xml_part_beats = etree.SubElement(xml_part_time, "beats")
    xml_part_beats.text = str(time_sig[0])
    xml_part_beat_type = etree.SubElement(xml_part_time, "beat-type")
    xml_part_beat_type.text = str(time_sig[1])

    # set stave count for parts
    # TODO: only set for stave count > 2
    xml_part_staves = etree.SubElement(xml_part_attributes, "staves")
    xml_part_staves.text = str(staff_count)

    # TODO: eventually we need a clef determinant
    xml_part_clef = etree.SubElement(xml_part_attributes, "clef")
    xml_part_clef_sign = etree.SubElement(xml_part_clef, "sign")
    xml_part_clef_sign.text = "G"
    xml_part_clef_line = etree.SubElement(xml_part_clef, "line")
    xml_part_clef_line.text = "2"

    return xml_measure