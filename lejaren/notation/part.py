import copy
import fractions, math
from itertools import accumulate, cycle

from lxml import etree
from typing import Iterable, List, Optional, NamedTuple, Tuple, Union

from .measure import Measure
from .note import Note
from .beat import Beat
from .rest import Rest
from .chord import Chord
import py2musicxml.log as logger

from py2musicxml.notation import measure

log = logger.get_logger()

# from collections import namedtuple

TimeSignature = Tuple[int, int]
TimeSignatures = List[Tuple[int, int]]


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
        time_signatures: TimeSignatures,
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

        time_signatures (tuple[TimeSignature]): a tuple of TimeSignature(s). If one TimeSignature
        is given, the entire part is that time signature. Otherwise, the Time Signatures are cycled
        through.

        key (int): pitch class for the major key of the desired key signature.

        clef (char): Letter Name for the clef for the part.

        line (int): line for the clef to be "centered" on.

        Returns:
        --------

        A Part object.

        """

        self.current_list = input_list

        for note in self.current_list:
            if note is type(Note):
                note._get_step_name(key)

        self.measures = []

        # TS stuff
        self.time_signatures = time_signatures
        self.time_signature_index = 0

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

        dur_uniques = self.get_note_uniques()
        denominator_uniques = self.get_ts_uniques()
        self.measure_factor = self._get_factor(dur_uniques) * max(denominator_uniques)

        # self.create_part(self.current_list, self.measure_factor)

        self.get_measures(self.current_list, self.time_signatures)

        [measure.clean_up_measure() for measure in self.measures]

    """default behavior is to simply clean an input list to 4/4
       it's also an option to feed extra arguments with keywords to 
       modify behavior for optional cleaning methods or user choices
       for measure groupings of factors"""

    def _test_for_low_bottom_time_sig(
        self, time_sig: TimeSignature, measure_factor: int
    ) -> int:
        """
        Evaulates if TimeSignature is valid or needs to be scaled.

        Arguments:
        ----------
        time_sig: a TimeSignature

        measure_factor (int): a scaling factor for the measure (usually acquired internally).

        """
        if time_sig[1] < 3:
            new_measure_factor = measure_factor * time_sig[1]
            return new_measure_factor
        elif time_sig[1] > 4:
            new_measure_factor = 4 / time_sig[1]
            return new_measure_factor
        else:
            return measure_factor

    def create_part(
        self, current_list: Iterable[Union[Note, Rest]], measure_factor: int
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

    def get_note_uniques(self) -> list:
        """
        Removes dupes of durs in list of Note objects.

        If a duration has yet to be listed, it appends it to the uniques. This is essential
        toward developing the factor, as note values are dependant upon being 1) integers,
        and 2) scaled to the time signature of the XML in MusicXML.

        Arguments:
        ----------

        None.

        Returns:
        --------

        uniques (list[int]): a list of unique durations in the current_list.


        """
        uniques = []
        for item in self.current_list:
            if item.dur not in uniques:
                uniques.append(item.dur)
            else:
                pass
        return uniques

    def get_ts_uniques(self) -> list:
        """unique durations of the notes in the list"""
        uniques = []
        for item in self.time_signatures:
            if item[1] not in uniques:
                uniques.append(item[1])
            else:
                pass
        return uniques

    def _get_factor(self, input_list: list) -> int:
        """
        Returns a factor (int) that scales all duration values to ints.

        Converts all durations to fractions, then finds the least common multiple. This is
        then returned as the factor to scale durations for MusicXML.

        Arguments:
        ----------

        input_list (list[float]): list of unique durations. (See _get_uniques).

        Returns:

        factor (int): scaling factor for MusicXML.

        """
        fractional_list = [
            fractions.Fraction(x).limit_denominator(128) for x in input_list
        ]
        denominators = [x.denominator for x in fractional_list]
        if denominators:
            lcm = denominators[0]
            for i in denominators[1:]:
                lcm = int(lcm * i / math.gcd(lcm, i))
            factor = lcm
        else:
            factor = 1

        return factor

    def _assign_measure_weight(self):
        """
        Assign weight for hypermetric ranking.

        Assigns a weight to the measure based on rules. Not yet implemented.

        Arguments:
        ----------

        None.

        Returns:
        --------

        None.
        """
        weight = 0
        for index, measure in enumerate(self.measures):
            self._get_change_pitch(10)

    def _compare_weight(self):
        pass

    def _get_index_range(self, index: int, search_range: int) -> Tuple[int, int]:
        """
        Returns range for searching for hypermetric analysis.

        Not yet implemented. Cleans a search range for beginning and ends of a list.

        Arguments:
        ----------

        index (int): location of note to compare in measure list.

        search_range (int): adjacent measures on both sides
        """
        if index < search_range:
            return 0, search_range + index
        else:
            return index - search_range, index + search_range

    def _get_change_pitch(self, index: int) -> None:
        """
        Tests the change in pitch between measure starts in search range and
        weights the measure appropriately.

        Evaluates the differences in measure pitch between search index, ranking a pitch
        that is a local maxima higher and weighting the measure accordingly.

        Arguments:
        ----------

        index (int): index of measure to evaulate.

        Returns:
        --------

        None, measure ranking is held in measure object.
        """
        index_range_low, index_range_high = self._get_index_range(index)
        test_measure_pitch = self.measures[index].beats[0]

        # test downbeats
        for measure in self.measures[index_range_low:index_range_high]:
            if measure.beats[0] > test_measure_pitch:
                break
            else:
                self.weight += 1
        for measure in self.measures:
            if measure.beats[0] < test_measure_pitch:
                break
            else:
                self.weight += 1

    def _get_change_group(self):
        """
        Placeholder.
        """
        pass

    def _get_implied_meter(self):
        """
        Evaluate note list to break into groupings of 2 and 3 and attempts to define
        metric weight and assigns a TimeSignature to groupings.

        Evaluates pitch strength in metric and hypermetric terms, and attempts to create
        a TimeSignature to subdivide note list. Not accurate, very risky, use at own risk.

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

    def _flatten_chords(
        self, note_list: Iterable[Union[Note, Rest, Chord]]
    ) -> Iterable[Union[Note, Rest]]:

        flat_list = []

        for idx, entry in enumerate(note_list):
            if type(entry) == Chord:
                flat_list.extend(entry.notes)
            else:
                flat_list.append(entry)

        return flat_list

    def _accum_note_durs(self, note_list: Iterable[Union[Note, Rest, Chord]]):

        dur_list = [entry.dur for entry in note_list]

        accumulated_durs = accumulate(dur_list)

        return accumulated_durs

    def _make_new_measure(
        self,
        time_signatures: TimeSignatures,
        current_measure: Measure,
        current_beat_count: int,
    ) -> Measure:

        time_sigs = cycle(time_signatures)

        next_ts = next(time_sigs)
        measure_max = next_ts[0]
        current_beat_count += next_ts[0]
        self.measures.append(current_measure)
        current_measure = Measure(next_ts, 1)

        return current_measure, current_beat_count, measure_max

    def get_measures(
        self, note_list: Iterable[Union[Note, Rest, Chord]], time_sigs: TimeSignatures
    ):

        accumulated_durs = self._accum_note_durs(iter(note_list))

        time_sigs = cycle(time_sigs)

        next_ts = next(time_sigs)
        current_beat_count = next_ts[0]
        measure_max = next_ts[0]
        current_measure = Measure(next_ts, 1)

        for current_count, note in zip(accumulated_durs, note_list):

            # import pdb; pdb.set_trace()

            if current_beat_count > current_count:
                current_measure.add_note(note)
            elif current_beat_count == current_count:
                current_measure.add_note(note)
                (
                    current_measure,
                    current_beat_count,
                    measure_max,
                ) = self._make_new_measure(
                    time_sigs, current_measure, current_beat_count
                )
            elif current_beat_count < current_count:
                diff = current_count - current_beat_count
                old_note, new_note = note.split(diff)
                current_measure.add_note(old_note)
                (
                    current_measure,
                    current_beat_count,
                    measure_max,
                ) = self._make_new_measure(
                    time_sigs, current_measure, current_beat_count
                )
                while diff > measure_max:
                    diff = diff - measure_max
                    old_note, new_note = new_note.split(diff)
                    current_measure.add_note(old_note)
                    (
                        current_measure,
                        current_beat_count,
                        measure_max,
                    ) = self._make_new_measure(
                        time_sigs, current_measure, current_beat_count
                    )
                if type(new_note) is not Rest:
                    new_note.set_as_tie("tie_end")
                current_measure.add_note(new_note)
        if current_measure.notes:
            self.measures.append(current_measure)
