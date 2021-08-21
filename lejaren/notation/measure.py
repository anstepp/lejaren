"""
The Measure object generally should not be called by a user.

Measure includes information that py2musicxml uses to keep
track of metric structure. 
"""

import copy
from itertools import accumulate

from typing import Iterable, List, Optional, Tuple, Union, List

from .note import Note
from .beat import Beat
from .rest import Rest
from .chord import Chord
import py2musicxml.log as logger

log = logger.get_logger()

METER_DIVISION_TYPES = {2: "Duple", 3: "Triple", 4: "Quadruple"}
TimeSignature = Tuple[int, int]


class Measure:

    """
    A class to represent a musical measure.

    Attributes:

    time_signature : Tuple(int, int)
    The time signature for the measure, with the first int representing
    the top note.

    beats : List(float)
    Collection of beat objects

    equal_divisions : bool
    Flag for if the measure is additive meter or not

    measure_number : int
    The measure's index + 1 in a part object.

    meter_division :
    subdivision of the meter by beat

    meter_type :
    The type of meter: simple, compound, etc

    measure_map : list
    A list of the values of the beats in the measure.

    cumulative_beats: list
    Additive list of the values of the beats in the measure.

    total_cumulative_beats : int
    Total addtitive beat count.

    Methods:
    --------

    is_empty()
    Tests for any beats in self.beats. Returns a bool.

    add_beat(Beat)
    Appends beat to the end of self.beats. You should append Notes to a
    Beat object, then append the Beat object.

    """

    def __init__(self, time_signature: Tuple, factor: int):

        """Init a measure with a time signature and factor. This
        sets all the relevant information about a measure.

        Arguments:
        ----------

        time_signature (Time Signature): a Time Signature tuple

        factor (int): unused scaling factor


        """

        self.time_signature = time_signature

        self.notes = []

        # A Measure contains a list of Beat objects
        self.beats = []

        # default to non-additive meter, this self corrects
        # equal divisions means all beats are the same, eg. 4/4, 6/8, but not 5/8
        self.equal_divisions = True

        # Measure number relative to order in Part()
        self.measure_number = None

        # hypermetric weight of measure
        # self.weight = None

        # factor for divisions
        self.measure_factor = factor

        (
            self.meter_division,
            self.meter_type,
            self.measure_map,
        ) = self._create_measure_map(self.measure_factor)

        self.cumulative_beats = list((x for x in self._cumulative_beat_generator()))
        self.total_cumulative_beats = self.cumulative_beats[-1]

    def _factorize_notes(self):

        note_durs = [note.dur for beat in self.beats for note in beat.notes]

        min_dur = min(note_durs)

        if min_dur < 1:
            self.measure_factor = 1 / min_dur
            for beat in self.beats:
                beat.subdivisions *= self.measure_factor
                for note in beat.notes:
                    note.change_duration(note.dur * self.measure_factor)
        else:
            pass

    def is_empty(self) -> bool:
        """Tests for an empty measure.

        Arguments:

        None.

        Returns:

        Bool.

        """
        if len(self.beats) == 0:
            return True
        else:
            return False

    def _cumulative_beat_generator(self) -> None:
        """Using the measure map, creates a list of the values for each beat
        that is cummulative. This is used in the Part.get_internal_measures
        method.

        Arguments:

        None

        Returns:

        None

        """
        count = 0
        for beat in self.measure_map:
            count += beat
            yield count

    def add_note(self, note: Note) -> None:
        """
        Add a beat to Measure.Beats, adding the notes inside the beat.

        Arguments:
        ----------

        beat: a Beat object with or without consitiuent notes.

        Returns:

        None

        """
        log.debug(f"Adding note to measure: {note}")
        self.notes.append(note)

    def extend_measure(self, note_list: Iterable[Union[Note, Rest, Chord]]):
        self.notes.extend(note_list)

    def add_beat(self, beat: Beat) -> None:

        """
        Add a beat to Measure.Beats, adding the notes inside the beat.

        Arguments:
        ----------

        beat: a Beat object with or without consitiuent notes.

        Returns:

        None

        """
        self.beats.append(beat)
        log.debug(f"Appending beat and len: {beat} {len(beat.notes)}")

    def set_time_signature(self, time_signature: TimeSignature) -> None:
        """For future use - eventally this should trigger a cascade
        measure rewrite in a part object that contains the re-sig'd
        measure.

        This should also consider allowing a rewrite of just the measure
        with rests to fill, or deletion of notes.
        """

        self.time_signature = time_signature
        self._create_measure_map(1)

    def _create_measure_map(self, factor: int) -> Tuple[Optional[str], str, List[int]]:
        """
        1. Determines the measure division and type
            (measure_type will always be Simple, Compound, or Additive)

        2. Creates and returns the measure map.
            measure map is a list of the beat durations in the measure; it maps out the beats of a measure

        Arguments:
        ----------

        factor: scaling factor for the internal notes.

        Returns:

        Tuple

        """

        meter_division = None
        meter_type = None
        measure_map = []

        if self.equal_divisions:

            if self.time_signature[0] >= 5 and self.time_signature[0] % 3 == 0:

                beats_in_measure = int(self.time_signature[0] / 3)

                meter_division = METER_DIVISION_TYPES.get(beats_in_measure, None)

                meter_type = "Compound"
                measure_map = [1.5 for x in range(beats_in_measure)]

            elif self.time_signature[0] <= 4:

                beats_in_measure = int(self.time_signature[0])

                meter_division = METER_DIVISION_TYPES.get(beats_in_measure, None)
                meter_type = "Simple"
                measure_map = [1 for x in range(beats_in_measure)]

            # time sig denominator is divisible by 4, but not 2
            elif ((self.time_signature[0] % 4) == 0) and (self.time_signature[0] > 2):

                beats_in_measure = self.time_signature[0]

                # print("Quadruple", beats_in_measure)

                meter_division = METER_DIVISION_TYPES.get(beats_in_measure, None)
                meter_type = "Simple"
                measure_map = [1 for x in range(beats_in_measure)]

            elif (self.time_signature[0] % 2) == 0:

                beats_in_measure = self.time_signature[0]

                # print("Duple", beats_in_measure)

                meter_division = METER_DIVISION_TYPES.get(beats_in_measure, None)
                meter_type = "Simple"
                measure_map = [1 for x in range(beats_in_measure)]

            elif self.time_signature[0] == 3:

                beats_in_measure = self.time_signature[0]

                meter_division = METER_DIVISION_TYPES.get(beats_in_measure, None)
                meter_type = "Simple"
                measure_map = [1 for x in range(beats_in_measure)]

            # time sig denominator is not divisible by 2 or 3
            else:
                # print("non div")
                self.equal_divisions = False

                beats_in_measure = self.time_signature[0]

                denominator = self.time_signature[1]

                divisions = int(beats_in_measure / 2)

                # meter_division remains None
                meter_type = "Additive"
                measure_map = self._front_load_measure(beats_in_measure, divisions)
                # measure_map = [factor / scale for x in range(beats_in_measure)]
        else:
            # meter_division remains None
            meter_type = "Additive"

        return meter_division, meter_type, measure_map

    def _front_load_measure(self, subdivisions: int, divisions: int):
        """front loads divisions on two numbers that are not divisible by each other"""

        return_list = [1 for x in range(divisions)]
        remainder = subdivisions - divisions

        idx = 0

        while remainder > 0:
            # print("_front_load_measure, remainder", remainder)
            return_list[idx] += 1
            idx = (idx + 1) % len(return_list)
            remainder -= 1

        return return_list

    def _test_multibeat(
        self,
        current_count: float,
        cumulative_beats: List[float],
        beat_divisions: List[int],
    ) -> Union[bool, int]:

        adj_count = current_count
        beats = cumulative_beats

        if adj_count in beats:
            for idx, val in enumerate(beats):
                log.debug(f"idx: {idx}, val: {val}, adj_count: {adj_count}")
                log.debug(f"beats sliced: {beats[:idx]}")
                if val == adj_count:
                    return True, beats[: idx + 1], beat_divisions[: idx + 1]
        else:
            return False, 0

    def _fill_measure(
        self,
        note_list: Iterable[Union[Note, Rest, Chord]],
        total_cumulative_beats: int,
    ) -> Iterable[Union[Note, Rest, Chord]]:

        # import pdb; pdb.set_trace()

        tot_durs = list(accumulate([note.dur for note in note_list]))[-1]

        if tot_durs < total_cumulative_beats:
            note_list.append(Rest(total_cumulative_beats - tot_durs))

        return note_list

    def clean_up_measure(
        self,
        note_list: Optional[Iterable[Union[Note, Rest, Chord]]] = None,
        total_cumulative_beats: Optional[float] = None,
    ) -> None:
        """Beams notes in the measure.

        To correctly beam notes, the function:
            * makes and groups beats in the measure
            * makes ties adds accidentals as necessary



        Arguments:
        ----------
        None

        Returns:
        --------
        None
        """

        # If we give a measure a set of notes, then this function will create the beats
        # and beam the notes correctly.
        # Beaming shows the beats in the measure, so it is easier to read for musicians
        # https://blogs.iu.edu/jsomcomposition/music-notation-style-guide/

        # Verify the measure is full

        if note_list is None:
            note_list = self.notes
        if total_cumulative_beats is None:
            total_cumulative_beats = self.total_cumulative_beats

        full_measure = self._fill_measure(note_list, total_cumulative_beats)

        new_beats = []

        # Reverse the notes and beats so that pop() takes them off
        # in order of appearance in the measure.
        notes = full_measure
        note_counter = len(notes)
        beat_divisions = self.measure_map
        current_beat_divisions = beat_divisions.pop()

        # cumulative beat count
        cumulative_beats = self.cumulative_beats
        cumulative_beats.reverse()
        beat_breakpoint = cumulative_beats.pop()

        log.debug(
            f"notes: {notes}, beat_divisions: {beat_divisions}, cumulative_beats: {cumulative_beats}"
        )

        # While there are notes to add
        current_count = 0
        current_beat = Beat(current_beat_divisions)
        for idx, note in enumerate(notes):

            # get initial states

            current_count += note.dur
            log.debug(
                f"Top: idx {idx}, note {note}, current count: {current_count}, current_beats: {self.beats}"
            )

            # inital test for multi-beat note (whole measure, etc.)
            if current_count in cumulative_beats:
                multi_beat, cumulative_beats, beat_divisions = self._test_multibeat(
                    current_count, cumulative_beats, beat_divisions
                )
                if cumulative_beats:
                    beat_breakpoint = cumulative_beats.pop()
                if beat_divisions:
                    current_beat_divisions = beat_divisions.pop()
                if multi_beat:
                    current_beat.multi_beat = True

            # previous note duration
            old_dur = 0
            note_for_next_beat = None
            was_equal = False

            # keep adding notes until we hit or break the breakpoint
            if current_count < beat_breakpoint:
                log.debug(f"Less Than: cc: {current_count}, bb: {beat_breakpoint}")
                current_beat.add_note(note)

            # add note and beat as we equal the breakpoint
            if current_count == beat_breakpoint:
                log.debug(f"Equal: cc: {current_count}, bb: {beat_breakpoint}")

                log.debug(f"appending: {note}")

                current_beat.add_note(note)

                self.add_beat(current_beat)
                if beat_divisions and cumulative_beats:
                    current_beat_divisions = beat_divisions.pop()
                    beat_breakpoint = cumulative_beats.pop()
                    current_beat = Beat(current_beat_divisions)

                was_equal = True

            # divide note into two parts - one for current beat, one for next beat
            elif current_count > beat_breakpoint:

                # tf, pops = self._test_multibeat(current_count, cumulative_beats)
                # if tf:
                #     for x in range(pops):
                #         current_beat_divisions = beat_divisions.pop()
                #         beat_breakpoint = cumulative_beats.pop()
                # else:
                #     pass

                log.debug(
                    f"current count > beat_breakpoint, {current_count}, {beat_breakpoint}"
                )

                overflow = current_count - beat_breakpoint
                log.debug(f"overflow, {overflow}, {current_count}, {beat_breakpoint}")
                remainder = note.dur - overflow
                if remainder > 0:
                    log.debug(f"remainder, {remainder}, {note.dur}")
                    old_beat_note = copy.deepcopy(note)
                    old_beat_note.change_duration(remainder)
                    old_beat_note.tie_start = True
                    current_beat.add_note(old_beat_note)
                    self.add_beat(current_beat)
                    if beat_divisions and cumulative_beats:
                        current_beat_divisions = beat_divisions.pop()
                        beat_breakpoint = cumulative_beats.pop()
                        current_beat = Beat(current_beat_divisions)
                    note_for_next_beat = copy.deepcopy(note)
                    note_for_next_beat.dur = overflow
                    current_beat.add_note(note_for_next_beat)

        self._factorize_notes()
        [beat.make_beams() for beat in self.beats]
