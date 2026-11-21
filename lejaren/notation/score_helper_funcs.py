from __future__ import annotations

from typing import TYPE_CHECKING

from lxml import etree

from .note import Note
from .part import Part
from .rest import Rest
from .chord import Chord
# avoid circular import
if TYPE_CHECKING:
    from .score import Score

from lejaren._constants import ARTICULATIONS, DIATONIC

from ._set_measure_attributes import _set_measure_attributes
from ._note_check import _note_check
from ._parse_parts import _parse_parts

import lejaren.log.log as logger
log = logger.get_logger()


def _convert_score_parts_to_xml(score: Score) -> etree.ElementTree:
    """Convert score.parts (list of NoteLists) to a MusicXML tree"""

    root = etree.Element("score-partwise", {"version": "4.0"})

    if score.title:
        xml_movement_title = etree.SubElement(root, "movement-title")
        xml_movement_title.text = score.title

    if score.composer:
        xml_identification = etree.SubElement(root, "identification")

        xml_identification_composer = etree.SubElement(
            xml_identification, "creator", {"type": "composer"}
        )

        xml_identification_composer.text = score.composer

    # create part-list
    #   score-part, part-name
    xml_part_list = etree.SubElement(root, "part-list")

    for idx, score_part in enumerate(score._parts):

        part_number = idx + 1

        xml_score_part = etree.SubElement(
            xml_part_list, "score-part", {"id": "P" + str(part_number)}
        )
        xml_part_name = etree.SubElement(xml_score_part, "part-name")

    # Write actual part, measures, notes, etc. to xml tree
    for part_idx, part in enumerate(score._parts):

        part_number = part_idx + 1
        xml_part = etree.SubElement(root, "part", {"id": "P" + str(part_number)})

        staff_count = part["staff_count"]
        staves = part["staves"]

        # Iterate through each Measure of the Part.
        for measure_index in range(score._measure_count):

            # xml measures are 1 indexed, but Measures are 0 indexed
            current_measure_count = measure_index + 1

            if current_measure_count <= score._measure_count:
                xml_measure = etree.SubElement(
                    xml_part, "measure", {"number": str(current_measure_count)}
                )

            # Iterate through each staff in the Part Measure.
            for staff_idx, staff in enumerate(staves):

                current_measure = staff.measures[measure_index]

                if (measure_index == 0) and (staff_idx == 0):
                    xml_measure = _set_measure_attributes(
                        xml_measure,
                        current_measure.time_signature,
                        staff.measure_factor,
                        staff_count,
                    )

                    xml_measure_attributes = etree.SubElement(
                        xml_measure, "attributes"
                    )
                    xml_measure_divisions = etree.SubElement(
                        xml_measure_attributes, "divisions"
                    )
                    xml_measure_divisions.text = str(current_measure.measure_factor)

                standard_subdivisions = []
                if current_measure_count != 1:
                    # xml_measure = etree.SubElement(
                    #     xml_part, "measure", {"number": str(current_measure_count)}
                    # )
                    if measure_index > 0:
                        xml_measure_attributes = etree.SubElement(
                            xml_measure, "attributes"
                        )
                        xml_measure_divisions = etree.SubElement(
                            xml_measure_attributes, "divisions"
                        )
                        xml_measure_divisions.text = str(current_measure.measure_factor)
                        # if time signature changes, reset attributes
                        if (
                            current_measure.time_signature
                            != staff.measures[measure_index - 1].time_signature
                        ):
                            xml_measure_time_signature = etree.SubElement(
                                xml_measure_attributes, "time"
                            )
                            xml_measure_time_beats = etree.SubElement(
                                xml_measure_time_signature, "beats"
                            )
                            xml_measure_time_beat_type = etree.SubElement(
                                xml_measure_time_signature, "beat-type"
                            )
                            xml_measure_time_beats.text = str(
                                current_measure.time_signature[0]
                            )
                            xml_measure_time_beat_type.text = str(
                                current_measure.time_signature[1]
                            )
                        else:
                            pass

                # we add the notes
                for current_beat in current_measure.beats:
                    beat_subdivisions = current_beat.subdivisions

                    for current_note in current_beat.notes:

                        if type(current_note) == Rest:
                            xml_note = etree.SubElement(xml_measure, "note")
                            xml_rest = etree.SubElement(xml_note, "rest")
                            xml_rest_duration = etree.SubElement(
                                xml_note, "duration"
                            )
                            xml_rest_duration.text = str(current_note.dur)

                        elif type(current_note) == Chord:
                            log.debug("CHORD")
                            pass

                        else:
                            # note
                            #   -> pitch, duration, accidental, notation ties
                            xml_note = etree.SubElement(xml_measure, "note")

                            if current_note.is_chord_member:

                                xml_chord_tag = etree.SubElement(xml_note, "chord")

                            xml_note_pitch = etree.SubElement(xml_note, "pitch")

                            # pitch step
                            xml_note_pitch_step = etree.SubElement(
                                xml_note_pitch, "step"
                            )
                            xml_note_pitch_step.text = current_note.step_name

                            # pitch alter
                            xml_note_pitch_alter = etree.SubElement(
                                xml_note_pitch, "alter"
                            )

                            xml_note_pitch_alter.text = (
                                current_note.alter
                                if xml_note_pitch_alter is not None
                                else 0
                            )

                            # pitch octave
                            xml_note_pitch_octave = etree.SubElement(
                                xml_note_pitch, "octave"
                            )
                            xml_note_pitch_octave.text = str(current_note.octave)

                            # duration
                            xml_note_duration = etree.SubElement(
                                xml_note, "duration"
                            )
                            xml_note_duration.text = str(current_note.dur)

                            if current_note.tie_start:
                                xml_tie = etree.SubElement(
                                    xml_note, "tie", {"type": "start"}
                                )

                            if current_note.tie_continue:
                                xml_tie = etree.SubElement(
                                    xml_note, "tie", {"type": "start"}
                                )

                            if current_note.tie_end:
                                xml_tie = etree.SubElement(
                                    xml_note, "tie", {"type": "stop"}
                                )

                            # accidental
                            if current_note.alter:
                                xml_note_accidental = etree.SubElement(
                                    xml_note, "accidental"
                                )
                                xml_note_accidental.text = current_note.accidental

                            # staff
                            xml_note_staff = etree.SubElement(xml_note, "staff")
                            xml_note_staff.text = str(staff_idx + 1)

                            # beam
                            if current_note.beam_start == True:
                                xml_beam = etree.SubElement(xml_note, "beam")
                                xml_beam.text = "begin"
                            elif current_note.beam_continue == True:
                                xml_beam = etree.SubElement(xml_note, "beam")
                                xml_beam.text = "continue"

                            # time modification
                            if current_beat.tuplet == True:
                                xml_time_modification = etree.SubElement(
                                    xml_note, "time-modification"
                                )
                                xml_time_modification_actual = etree.SubElement(
                                    xml_time_modification, "actual-notes"
                                )
                                xml_time_modification_actual.text = str(
                                    current_beat.actual_notes
                                )
                                xml_time_modification_normal = etree.SubElement(
                                    xml_time_modification, "normal-notes"
                                )
                                xml_time_modification_normal.text = str(
                                    current_beat.subdivisions
                                )

                            # notation ties
                            if current_note.tie_start:
                                xml_notations = etree.SubElement(
                                    xml_note, "notations"
                                )
                                xml_notations_tied = etree.SubElement(
                                    xml_notations, "tied", {"type": "start"}
                                )
                            if current_note.tie_continue:
                                xml_notations = etree.SubElement(
                                    xml_note, "notations"
                                )
                                xml_notations_tied = etree.SubElement(
                                    xml_notations, "tied", {"type": "continue"}
                                )
                            if current_note.tie_end:
                                xml_notations = etree.SubElement(
                                    xml_note, "notations"
                                )
                                xml_notations_tied = etree.SubElement(
                                    xml_notations, "tied", {"type": "stop"}
                                )

                            if current_note.articulation:
                                if current_note.articulation in ARTICULATIONS:
                                    xml_notations = etree.SubElement(
                                        xml_note, "notations"
                                    )
                                    xml_notations_articulation = etree.SubElement(
                                        xml_notations, "articulations"
                                    )
                                    xml_articulation = etree.SubElement(
                                        xml_notations_articulation,
                                        current_note.articulation,
                                    )
                            else:
                                log.warning(f"No operations performed on element:")

                if (len(staves) > 1) and (staff_idx < len(staves) - 1):
                    xml_backup = etree.SubElement(xml_measure, "backup")
                    xml_backup_duration = etree.SubElement(xml_backup, "duration")
                    xml_backup_duration.text = str(
                        staff.measure_factor
                        * current_measure.total_cumulative_beats
                    )

        serialized = etree.tostring(
            root,
            #TODO: Choose - make like to remote or have local pull in repo
            doctype='<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" "http://www.musicxml.org/xsd/musicxml.xsd">',
        )

        new_root = etree.XML(serialized)
        musicxml_tree = etree.ElementTree(new_root)

        part_number += 1

    return musicxml_tree

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