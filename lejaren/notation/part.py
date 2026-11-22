from itertools import accumulate, cycle

from typing import Iterable, NamedTuple, Union

from lejaren._types import TIME_SIGNATURES, NOTE_LIST, NO_CHORDS
from lejaren._constants import MAX_LINES, CLEFS

from .measure import Measure
from .note import Note
from .rest import Rest
from .chord import Chord

from .part_funcs.extract_note_list_from_range import extract_note_list_from_range
from .part_funcs._flatten_chords import _flatten_chords
from .part_funcs._test_for_low_bottom_time_sig import _test_for_low_bottom_time_sig
from .part_funcs.check_uniques import _get_factor
from .part_funcs._get_index_range import _get_index_range
from .part_funcs._make_new_measure import _make_new_measure

import lejaren.log.log as logger
log = logger.get_logger()

class CurrentCountDivisions(NamedTuple):
    """
    A class containing all the relevant divisions related to current_count.

    A class to be invoked to keep track of various subdivisions needed
    when grouping the current_list into Beat objects inside Measure objects.
    Should not be created or called by the end user.

    Attributes:
    -----------

    beat_floor (int): floor division of current_count the remainder of
    current_note

    beat_mod (int): modulo division of current_count and the remainder of
    current_note

    measure_floor (int): floor divsion of current_count and the max measure divsions

    measure_mod (int): mod division of current_count and the max measure divisions

    Methods:
    --------

    set_and_return_adjacencies

    """

    beat_floor: int
    beat_mod: int
    measure_floor: int
    measure_mod: int


class Part:

    """
    The part class represents a musical part. A Part can contain more than
    one staff.

    A part object can be invoked inside an instrument.

    Attributes:
    -----------

    current_list: a list of note objects that can be operated upon

    measures: a list of measures. This begins empty, and is created when
    _get_measure_list() is invoked inside create_part on instantiation.

    time_signatures: a list or singleton of time_signatures that is cycled
    over to generate each measure's time signature.

    time_signature_index: a counter for the current time signature.

    subdivisions:

    max_subdivisions:

    current_beat_count:

    current_measure:

    current_count_mod:

    current_count_floor:

    measure_factor:

    Methods:
    --------

    create_part: create the part with the current Time Signatures.

    """

    def __init__(
        self,
        input_list: Iterable[Note],
        # TODO/FIXME: Verify Time Signature on instantiation
        time_signatures: TIME_SIGNATURES,
        key=0,
        clef="G",
        line=2,
    ):
        """
        Create a Part object.

        Creating a Part object sets off a cascade of events, creating a list of Measure objects
        containing Beat objects, containing Note objects. Measures should generally not be created
        directly by the end user, but through modifying the note list, then calling create_part().
        Otherwise, there is no guarantee that the measure object is accurately taken into account
        with the other arguments given.

        Arguments:
        ----------

        input_list (list[Note]): a list of Note objects. They can be of any duration.

        time_signatures (tuple[TIME_SIGNATURE]): a tuple of TIME_SIGNATURE(S). If one TIME_SIGNATURE
        is given, the entire part is that time signature. Otherwise, the Time Signatures are cycled
        through.

        key (int): pitch class for the major key of the desired key signature.

        clef (char): Letter Name for the clef for the part.

        line (int): line for the clef to be "centered" on.

        Returns:
        --------

        A Part object.

        """

        if isinstance(input_list, list):
            self.current_list = input_list
        elif isinstance(input_list, Note|Rest):
            log.debug("Wrapping Single Note/Rest in List")
            self.current_list = [input_list]
        else:
            warnstr = f"Bad Note list to Part, is type: {type(input_list)}"
            log.warning(warnstr)
            raise ValueError(warnstr)

        for note in self.current_list:
            if note is type(Note):
                note._get_step_name(key)

        self.measures = []

        # Time Signature stuff
        # FIXME: use lejaren._types
        try:
            isinstance(time_signatures, (list|tuple))
        except TypeError as e:
            warnstr = f"Time Signature non-usable, was type: {type(time_signatures)}, details: {e}"
            log.warning(warnstr)
            print(warnstr)
        if not isinstance(time_signatures, list):
            log.debug("Wrapping Time Signature in List")
            self.time_signatures = [time_signatures]
        else:
            self.time_signatures = time_signatures

        self.time_signature_index: int = 0

        self.subdivisions, self.max_subdivisions = None, None

        # where we are in the cumulative beats
        self.current_measure = None
        # value of note duration that needs to be written
        # current count gets incremented when we intake the next note
        # gets decremented when we write a measure
        self.current_count = 0

        # current count mod or floor divided by current cumulative beat
        self.current_count_mod, self.current_count_floor = None, None

        #  self.current_measure_mod, self.current_measure_floor


        self.measure_factor = _get_factor(self.current_list, self.time_signatures)

        self.get_measures(self.current_list, self.time_signatures)

        [measure.clean_up_measure() for measure in self.measures]

        if clef not in CLEFS:
            warnstr = f"Clef not real, was: {clef}"
            log.warning(warnstr)
            raise ValueError(warnstr)
        else:
            self.clef = clef
        if line < MAX_LINES and line > 0:
            self.line = line
        else:
            warnstr = f"Can't have a clef on over 5 lines, was: {line}"
            log.warning(warnstr)
            raise ValueError(warnstr)

    """default behavior is to simply clean an input list to 4/4
       it's also an option to feed extra arguments with keywords to 
       modify behavior for optional cleaning methods or user choices
       for measure groupings of factors"""

    def create_part(
        self, current_list: NO_CHORDS, measure_factor: int
    ) -> None:
        """
        Transform input list of notes into a list of measures.

        Wrapper function for the plethora of actions taken to divide the current_list into
        measures.

        Arguments:
        ----------

        None.

        Returns:
        --------

        Nothing. List is handled internally.
        """

        # set all durations to be factored
        [note.change_duration(note.dur * measure_factor) for note in current_list]

        self._group_list_to_measures(current_list, measure_factor)
    

    def _get_change_group(self):
        """
        Placeholder.
        """
        pass

    def _get_implied_meter(self):
        """
        Evaluate note list to break into groupings of 2 and 3 and attempts to define
        metric weight and assigns a TIME_SIGNATURE to groupings.

        Evaluates pitch strength in metric and hypermetric terms, and attempts to create
        a TIME_SIGNATURE to subdivide note list. Not accurate, very risky, use at own risk.

        Arguments:
        ----------

        None.

        Returns:
        --------

        None.
        """
        location_map = []
        pitch_locations = self.get_change_pitch()
        meter_locations = self.get_change_group()
        highest_level = [
            pitch
            for pitch, meter in zip(pitch_locations, meter_locations)
            if pitch == meter
        ]
        last_location = 0
        # perhaps wrap this in a smaller function and make it recurisve? Is there a non-recusrive way to make this work?
        for location in highest_level:
            subgroup = self.current_list[last_location:location]
            groups_2_and_3 = self.metric_finder(
                subgroup
            )  # or should I use the .get_change_pitch() and .get_change_group()
            location_map.append(groups_2_and_3)
            location = last_location
        implied_list = self.group_by_map(location_map)
        return implied_list

    def _accum_note_durs(self, note_list: Iterable[Union[Note, Rest, Chord]]):

        dur_list = [entry.dur for entry in note_list]

        accumulated_durs = accumulate(dur_list)

        return accumulated_durs



    def get_measures(
        self, note_list: NOTE_LIST, time_sigs: TIME_SIGNATURES
    ):

        accumulated_durs = self._accum_note_durs(iter(note_list))

        time_sigs = cycle(time_sigs)

        next_ts = next(time_sigs)
        current_beat_count = next_ts[0]
        measure_max = next_ts[0]
        current_measure = Measure(next_ts, 1)

        for current_count, note in zip(accumulated_durs, note_list):

            if current_beat_count > current_count:
                current_measure.add_note(note)
            elif current_beat_count == current_count:
                current_measure.add_note(note)
                (
                    self.measures, 
                    current_measure, 
                    current_beat_count,
                    measure_max,
                ) = _make_new_measure(
                    self.measures, 
                    time_sigs, 
                    current_measure, 
                    current_beat_count
                )
            elif current_beat_count < current_count:
                diff = current_count - current_beat_count
                old_note, new_note = note.split(diff)
                current_measure.add_note(old_note)
                (
                    self.measures, 
                    current_measure, 
                    current_beat_count,
                    measure_max,
                ) = _make_new_measure(
                    self.measures, 
                    time_sigs, 
                    current_measure, 
                    current_beat_count
                )
                while diff > measure_max:
                    diff = diff - measure_max
                    old_note, new_note = new_note.split(diff)
                    current_measure.add_note(old_note)
                    (
                        self.measures, 
                        current_measure, 
                        current_beat_count,
                        measure_max,
                    ) = _make_new_measure(
                        self.measures, 
                        time_sigs, 
                        current_measure, 
                        current_beat_count
                    )
                if type(new_note) is not Rest:
                    new_note.set_as_tie("tie_end")
                current_measure.add_note(new_note)
        if current_measure.notes:
            self.measures.append(current_measure)

