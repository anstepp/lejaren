import pathlib

from lxml import etree
from typing import Iterable, Optional, Tuple

from .part import Part
from .rest import Rest
from .measure import Measure
from .beat import Beat
from .chord import Chord
import py2musicxml.log as logger

log = logger.get_logger()

EMPTY_MEASURE_FACTOR = 1

class Score:
    """Generates a MusicXML score from a list of parts (NoteLists) and outputs score to file"""

    def __init__(
        self,
        parts: Iterable[Iterable[Part]],
        title: Optional[str] = None,
        composer: Optional[str] = None,
    ):
    
        self.title = title
        self.composer = composer

        self._parts = self._parse_parts(parts)
        self._measure_count = self._pad_with_empty_measures()

    def _parse_parts(self, parts):

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
            raise Exception("Invalid parts argument supplied to Score.")

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
        xml_score = self._convert_score_parts_to_xml()
        self._write_xml_to_file(output_filepath, xml_score)

    def _set_measure_attributes(
        self,
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

    def _convert_score_parts_to_xml(self) -> etree.ElementTree:
        """Convert self.parts (list of NoteLists) to a MusicXML tree"""

        root = etree.Element("score-partwise", {"version": "3.0"})

        if self.title:
            xml_movement_title = etree.SubElement(root, "movement-title")
            xml_movement_title.text = self.title

        if self.composer:
            xml_identification = etree.SubElement(root, "identification")

            xml_identification_composer = etree.SubElement(
                xml_identification, "creator", {"type": "composer"}
            )

            xml_identification_composer.text = self.composer

        # create part-list
        #   score-part, part-name
        xml_part_list = etree.SubElement(root, "part-list")

        for idx, score_part in enumerate(self._parts):

            part_number = idx + 1

            xml_score_part = etree.SubElement(
                xml_part_list, "score-part", {"id": "P" + str(part_number)}
            )
            xml_part_name = etree.SubElement(xml_score_part, "part-name")

        # Write actual part, measures, notes, etc. to xml tree
        for part_idx, part in enumerate(self._parts):

            part_number = part_idx + 1
            xml_part = etree.SubElement(root, "part", {"id": "P" + str(part_number)})

            staff_count = part["staff_count"]
            staves = part["staves"]

            # Iterate through each Measure of the Part.
            for measure_index in range(self._measure_count):

                # xml measures are 1 indexed, but Measures are 0 indexed
                current_measure_count = measure_index + 1

                if current_measure_count <= self._measure_count:
                    xml_measure = etree.SubElement(
                        xml_part, "measure", {"number": str(current_measure_count)}
                    )

                # Iterate through each staff in the Part Measure.
                for staff_idx, staff in enumerate(staves):

                    current_measure = staff.measures[measure_index]

                    if (measure_index == 0) and (staff_idx == 0):
                        xml_measure = self._set_measure_attributes(
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
                                    pass

                    if (len(staves) > 1) and (staff_idx < len(staves) - 1):
                        xml_backup = etree.SubElement(xml_measure, "backup")
                        xml_backup_duration = etree.SubElement(xml_backup, "duration")
                        xml_backup_duration.text = str(
                            staff.measure_factor
                            * current_measure.total_cumulative_beats
                        )

            serialized = etree.tostring(
                root,
                doctype='<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">',
            )

            new_root = etree.XML(serialized)
            musicxml_tree = etree.ElementTree(new_root)

            part_number += 1

        return musicxml_tree

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
