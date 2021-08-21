"""
The Note object contains and represents notes with pitch and duration.
Pitches are represented in two domains: octave and pitch class. Each
is a separate data member, and can be modified separately. Duration
is one member.

Because the Measure and Part objects contain code to split notes across
measures, you can create a list of Notes objects and not split them for
the measure. This is useful for prototyping.

Users should only need to instantiate a Note object, or use the overloaded 
math operators. To create a note, simply create the object:

>>> middle_C_whole_note = Note(4,4,0)

The Note object overloads operators to allow for comparison of note objects.
There is an attempt to be intutitive. Equality tests for pitches, greater
than/less than test for pitch relationships, and greater than or equal/less
than or equal test for duration relationships. As follows:

note_1 = Note(4,4,0) # Whole note middle C
note_2 = Note(2,4,1) # Half note middle C#

>>> note_1 == note_2 # Middle C is not Middle C-sharp
False
>>> note_1 > note_2 # Middle C is lower than Middle C-sharp
False
>>> note_1 >= note_2 # A whole note is longer than a half note
True

"""

import copy
from typing import Tuple

import py2musicxml.log as logger

log = logger.get_logger()

# The Life of a Note

# in a tuplet, we change the subdivision of the beat
# groups of 3 in the space of 2
# grouping of notes other than the subdivision of the meter
# it has to change in the subdivsion, feel of music changes
# how is this unit of time divided, and then subdivided

# when beat is divided by 2, subdivisions are in groups of 2 - simple time
# by 3, compound
# 4 is outgrowth of 2, can be reduced into 2


class Note:
    """
    A class to represent a musical note.

    Attributes:
    -----------
    dur : float
    represents the duration of the note

    octave : int
    the octave of the note

    pc : int (0-11)
    the pitch class of the note, gets corrected if outside the 0-11 interval

    step_name : str
    letter name of pitch

    alter : int
    alteration up/down of pitch

    accidental : str
    string representation of accidental for the note

    tie_start, tie_continue, tie_end : bool
    flags for ties on the note

    tuplet_start, tuplet_continue, tuplet_end : bool
    flags for tuplet presentation (not actual values)

    beam_start, beam_continue : bool
    beaming flags for the note

    is_chord_member : bool
    flag for chord membership

    Methods:
    --------

    fix_pitch_overflow(self, octave: int, pitch_class: int)

    _get_step_name(self, starting_pitch: int)

    add_articulation(self, notation: str)

    set_as_tie(self, tie_type: str)

    Overloaded Operators:
    ---------------------

    == : absolute equality (dur, pc, octave)
    >/< : pitch greater than/less than
    >=/<= : duration greater than/less than

    """

    # default flags for ties & tuplets
    tie_start, tie_continue, tie_end = False, False, False
    tuplet_start, tuplet_continue, tuplet_end = False, False, False
    beam_start, beam_continue = False, False

    # measure defaults
    measure_factor, measure_flag = 1, False

    # chord
    is_chord_member = False

    def __init__(self, duration: float, octave: int, pitch_class: int) -> None:

        """Init a note with duration, octave and pc. Sets additional
        data members step_name, alter and accidental with _get_step_name
        as well as initing articulation.

        Arguments:

        duration (float): note duration

        octave (int): scientific octave of pitch

        pitch_class (int): pitch class of note (0-11)

        Returns:

        None

        """

        try:
            if duration > 0:
                self.dur = duration
        except ValueError as e:
            log.error(e)
            raise

        # called to correct any errant pitch classes
        self.octave, self.pc = self._fix_pitch_overflow(octave, pitch_class)

        # force starting_pitch to be keyless
        self.step_name, self.alter, self.accidental = self._get_step_name(0)

        self.articulation = None

    def _fix_pitch_overflow(self, octave: int, pitch_class: int) -> Tuple[int, int]:
        """
        Addresses pitch classes below 0 or above 11.

        Called on init to make sure pitch_class is mod12. If not, does
        math to corret pitch_class and octave. Because this is called on init,
        end user may need to call if a Note object is changed.

        Arguments:

        octave (int): octave of note

        pitch_class (int): pitch class of note

        """
        new_pitch_class, new_octave = None, None

        if pitch_class > 11:
            new_pitch_class = pitch_class % 12
            new_octave = octave + pitch_class // 12
            return new_octave, new_pitch_class

        elif pitch_class < 0:
            new_pitch_class = pitch_class % 12
            new_octave = octave + pitch_class // 12
            return new_octave, new_pitch_class

        else:
            return octave, pitch_class

    def _get_step_name(self, starting_pitch: int) -> Tuple[str, int, str]:

        """Used to get detailed information about a Note object's
        letter name, pitch class, and accidental.

        Uses lookup tables to get various nomeclature for representing
        pitch in XML. Key can be selected to default to simple spellings
        in key signature (dense chromaticism will not necessarily be
        correct). Neutral between MusicXML and MEI.

        Arguments:

        starting_pitch (int): pitch class to represent major key of
        key signature.

        Returns:

        Tuple: str (pitch class), int (accidental), str (accidental name)

        """

        flat_keys = [1, 3, 5, 8, 10]
        sharp_keys = [2, 4, 6, 7, 9, 11]

        step_names = {}

        if starting_pitch == 0:
            step_names = {
                0: ["C", "0", "natural"],
                1: ["C", "1", "sharp"],
                2: ["D", "0", "natural"],
                3: ["E", "-1", "flat"],
                4: ["E", "0", "natural"],
                5: ["F", "0", "natural"],
                6: ["F", "1", "sharp"],
                7: ["G", "0", "natural"],
                8: ["A", "-1", "flat"],
                9: ["A", "0", "natural"],
                10: ["B", "-1", "flat"],
                11: ["B", "0", "natural"],
            }
        elif starting_pitch in flat_keys:
            step_names = {
                0: ["C", "0", "natural"],
                1: ["D", "-1", "flat"],
                2: ["D", "0", "natural"],
                3: ["E", "-1", "flat"],
                4: ["E", "0", "natural"],
                5: ["F", "0", "natural"],
                6: ["G", "-1", "flat"],
                7: ["G", "0", "natural"],
                8: ["A", "-1", "flat"],
                9: ["A", "0", "natural"],
                10: ["B", "-1", "flat"],
                11: ["B", "0", "natural"],
            }
        elif starting_pitch in sharp_keys:
            step_names = {
                0: ["C", "0", "natural"],
                1: ["C", "1", "sharp"],
                2: ["D", "0", "natural"],
                3: ["D", "1", "sharp"],
                4: ["E", "0", "natural"],
                5: ["F", "0", "natural"],
                6: ["F", "1", "sharp"],
                7: ["G", "0", "natural"],
                8: ["G", "1", "sharp"],
                9: ["A", "0", "natural"],
                10: ["A", "1", "sharp"],
                11: ["B", "0", "natural"],
            }
        else:
            raise ValueError("starting_pitch must be zero, a flat key, or sharp key")

        return step_names[self.pc]

    def add_articulation(self, articulation: str) -> None:

        valid_articulations = [
            "accent",
            "breath-mark",
            "caesura",
            "detached-legato",
            "doit",
            "falloff",
            "plop",
            "scoop",
            "spiccato",
            "staccatissimo",
            "staccato",
            "stress",
            "strong-accent",
            "tenuto",
            "unstress",
        ]

        if articulation in valid_articulations:

            self.articulation = articulation

        else:

            raise ValueError(
                f"Articulation {articulation} must be a valid articulation: {valid_articulations}"
            )

    def set_as_tie(self, tie_type: str) -> None:
        """Sets note as a tied note of a specific type.

        By feeding a type of tie: start, continue, or end, add a tie to the note both
        in Py2MusicXML and the resulting XML. This can be called by an end user, or
        internally when breaking notes into measure groupings.

        Arguments:

        tie_type: either tie_start, tie_continue, or tie_end. Flags that specific note as
        that type of tie.

        Returns:

        None

        """

        if tie_type == "tie_start":
            self.tie_start = True
        elif tie_type == "tie_continue":
            self.tie_continue = True
            self.articulation = None
        elif tie_type == "tie_end":
            self.tie_end = True
            self.articulation = None
        else:
            raise Exception(
                f"Wrong Tie Type: tie_start, tie_continue, tie_end accepted, not {tie_type}"
            )

    def change_duration(self, new_duration: float) -> None:
        try:
            if new_duration > 0:
                self.dur = new_duration
        except ValueError as e:
            log.error(e)
            raise

    def split(self, diff: int) -> Tuple["__class__", "__class__"]:
        old_note = copy.copy(self)
        new_note = copy.copy(self)

        old_note.change_duration(self.dur - diff)
        old_note.set_as_tie("tie_start")

        new_note.change_duration(diff)

        return old_note, new_note

    def __eq__(self, other) -> bool:
        """
        Absolute equality test for two notes.

        Tests equality of duration, octave, and pitch class for two
        notes. Testing Note == Note is expected usage.

        Arguments:

        other (Note): a note to test equality.

        Returns:

        bool
        """

        if (
            (self.dur == other.dur)
            and (self.octave == other.octave)
            and (self.pc == other.pc)
        ):
            return True
        else:
            return False

    # Evaluate pitch relative to another

    def __gt__(self, other) -> bool:
        """
        Tests for pitch inequality.

        Arguments:

        other (Note): a Note object.
        """

        if self.octave > other.octave:
            return True
        elif self.octave == other.octave:
            if self.pc > other.pc:
                return True
            else:
                return False
        else:
            return False

    # Evaluate duration equality

    def __ge__(self, other) -> bool:
        """
        Tests for duration inequality.

        Arguments:

        other (Note): a Note object
        """
        if self.dur > other.dur:
            return True
        else:
            return False

    # Pretty printing in output

    def __str__(self) -> str:

        """
        Pretty print for core data members of the Note object

        Arguments:

        None (operates on self).

        Returns:

        string to stdout.
        """

        return "Duration: {}, Octave: {}, Pitch Class: {}".format(
            self.dur, self.octave, self.pc
        )
