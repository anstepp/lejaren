"""
Voice is a file that contains classes that represent voices and instruments.

To use one of the voices, you import:

from py2musicxml.composition import [chosen_voice]

The score then has access to creating an instrument:

first_trumpet = Trumpet()

Which you can then call methods that are either generic
or instrument specific. These methods allow for various
prototyping/score production functionality.

All instruments have the following methods. The necessary
arguments are given as well:

To extend pitch values:
Voice.extend_pitches(List[int])

To extend duration values:
Voice.extend_durations(List[int])

To convert pitch and duration values to Note objects:
Voice.make_note_list(int)

To add Note objects to the list of Note objects:
Voice.extend_note_list(List[Note, Rest])

To insert a Rest object of a given duration in the Note object list:
Voice.insert_rest(int: duration, int: index)

To insert a Note object or list of Note objects in the Note object list:
Voice.insert_note_list(List[Note, Rest], int: index)

Convert list of Note objects to a Part object:
Voice.make_part(Time_Signature)

Check range of the instrument:
Voice.check_range()

To clear out the note list:
Voice.clear_list()
"""

from py2musicxml.notation import Note, Rest, Part

from typing import List, Tuple, Iterable, Union

Time_Signature = List[Tuple[int, int]]
Range = List[Tuple[int, int]]
Slice = Tuple[int, int]

class Voice:
    def __init__(self):
        self.pitches = []
        self.durations = []

        self.inst_range = Range

        """Have both a note_list and a part associated with the instrument.
        In the case we have to operate a method belonging to an instrument
        after the measure/beat subdivision algorithm, or if the instrument
        is multiple parts (i.e. piano)"""
        self.note_list = []


        """default to treble clef"""

        self.clef = 'G'

        """Default to in c"""

        self.transposition = 0

    def _transpose(self, input_list: Iterable[Union[Note, Rest]], interval: int) -> None:

        temp_list = []

        for note in input_list:
            if isinstance(note, Note):
                temp_list.append(Note(note.dur, note.octave, note.pc + 2))
            else:
                temp_list.append(note)

        return temp_list

    def extend_pitches(self, input_list: list) -> None:
        self.pitches.extend(input_list)

    def extend_durations(self, input_list: list) -> None:
        self.durations.extend(input_list)

    def make_note_list(self, octave: int) -> None:
        self.note_list = [
            Note(dur, octave, pc) for dur, pc in zip(self.durations, self.pitches)
        ]

    def append_to_note_list(self, note: Iterable[Union[Note, Rest]]) -> None:
        self.note_list.append(note)

    def extend_note_list(self, input_list: Iterable[Union[Note, Rest]]) -> None:
        self.note_list.extend(input_list)

    def insert_rest(self, duration: int, index: int) -> None:
        self.note_list.insert(index, Rest(duration))

    def insert_note_list(self, input_list: Iterable[Union[Note, Rest]], index: int) -> None:
        first_chunk = self.note_list[0:index]
        last_chunk = self.note_list[index:]
        self.note_list = first_chunk + input_list + last_chunk

    def make_part(self, time_signature: Time_Signature) -> Part:
        checked_list = self._check_range(self.note_list)
        part = Part(checked_list, time_signature)
        return [part]

    def _check_range(self, note_list: Iterable[Union[Note, Rest]], temp_range=None):
        temp_list = []
        if temp_range:
            checking_range = temp_range
        else:
            checking_range = self.inst_range
        for note in note_list:
            if isinstance(note, Note):
                if note.octave == checking_range[0][0] and note.pc < checking_range[0][1]:
                    temp_note = Note(note.dur, note.octave + 1, note.pc)
                    temp_list.append(temp_note)

                elif note.octave == checking_range[0][0] and note.pc >= checking_range[0][1]:
                    temp_list.append(note)

                elif note.octave < checking_range[0][0]:
                    temp_note = Note(note.dur, checking_range[0][0], note.pc)
                    temp_list.append(temp_note)

                elif note.octave == checking_range[1][0] and note.pc > checking_range[1][1]:
                    temp_note = Note(note.dur, note.octave - 1, note.pc)
                    temp_list.append(temp_note)

                elif note.octave == checking_range[1][0] and note.pc <= checking_range[1][1]:
                    temp_list.append(note)

                elif note.octave > checking_range[1][0]:
                    temp_note = Note(note.dur, checking_range[1][0], note.pc)
                    temp_list.append(temp_note)  

                else:
                    temp_list.append(note)

            else:
                temp_list.append(note)

        return temp_list

    def make_staccato(self, slice_range=None) -> None:
        temp_list = []
        if slice_range:
            for note in self.note_list:
                if isinstance(note, Note) and note.dur >= 0.5:
                    temp_list.append(Note(0.25, note.octave, note.pc))
                    temp_list.append(Rest(note.dur - 0.25))
        else:
            for note in self.note_list:
                if isinstance(note, Note) and note.dur >= 0.5:
                    temp_list.append(Note(0.25, note.octave, note.pc))
                    temp_list.append(Rest(note.dur - 0.25))
        self.note_list = temp_list

    def clear_list(self):
        self.pitches = []
        self.durations = []
        self.note_list = []

    def set_note_list(self, input_list: Iterable[Union[Note, Rest]]) -> None:
        self.note_list = input_list

    def constrain_range(self, temp_range: Range):
        self.note_list = self._check_range(self.note_list, temp_range=temp_range)

# Woodwinds --------------------------------------------

class Woodwind(Voice):
    '''Needs woodwind specific information. Futher sub-classes
    can be created to adapt to the needs of each specific instrument.'''
    def __init__(self):
        super(Woodwind, self).__init__()

class Flute(Woodwind):
    def __init__(self):
        super(Flute, self).__init__()
        self.inst_range = [(4, 0), (7, 2)]
        self.clef = "G"

class Oboe(Woodwind):
    def __init__(self):
        super(Oboe, self).__init__()
        self.inst_range = [(4,10),(7,9)]
        self.clef = "G"

class Clarinet(Woodwind):
    def __init__(self):
        super(Clarinet, self).__init__()
        self.inst_range = [(3, 4), (6, 9)]
        self.chalumeau = [(3, 4), (4, 4)]
        self.clef = "G"
        self.transposition = 2

    def make_part(self, time_signature: Time_Signature) -> Part:
        checked_list = self._check_range(self.note_list)
        part = Part(checked_list, time_signature)
        return [part]

    def constrain_to_chalumeau(self) -> None:
        constrained_range = self._check_range(self.note_list, temp_range=self.chalumeau)
        self.note_list = constrained_range

class BassClarinet(Woodwind):
    def __init__(self):
        super(BassClarinet, self).__init__()
        self.inst_range = [(3,4),(3,6)]
        self.clef = "G"
        self.transposition = 16 # major 9th up

class Bassoon(Woodwind):
    def __init__(self):
        super(Bassoon, self).__init__()
        self.inst_range = [(1, 10), (5, 3)]
        self.clef = 'F'

# Brass -------------------------------------------------------

class Brass(Voice):
    def __init__(self):
        super(Brass, self).__init__()

class Trumpet(Brass):
    def __init__(self):
        super(Trumpet, self).__init__()
        self.inst_range = [(3,6),(6,0)]

class Horn(Brass):
    def __init__(self):
        super(Horn, self).__init__()
        self.inst_range[(2,6),(6,0)]

class Trombone(Brass):
    def __init__(self):
        super(Trombone, self).__init__()
        self.inst_range[(2,4),(5,7)]

class Tuba(Brass):
    def __init__(self):
        super(Tuba, self).__init__()
        self.inst_range[(0,2),(4,7)]


# Strings -----------------------------------------------------

class Strings(Voice):
    def __init__(self):
        super(Strings, self).__init__()
        self.open_strings = None

    def bariolage(self, range_to_affect: Slice) -> None:
        pass


class Violin(Strings):
    def __init__(self):
        super(Violin, self).__init__()
        self.inst_range = [(3, 7), (8, 11)]
        self.open_strings = [(3, 7), (4, 2), (4, 9), (5, 4)]
        self.clef = 'G'

class Viola(Strings):
    def __init__(self):
        super(Viola, self).__init__()
        self.inst_range = [(2, 0), (6, 11)]
        self.open_strings = [(2, 0), (2, 7), (3, 2), (3, 9)]


class Cello(Strings):
    def __init__(self):
        super(Cello, self).__init__()
        self.inst_range = [(1, 0), (6, 4)]
        self.open_strings = [(1, 0), (1, 7), (2, 2), (2, 9)]
        self.clef = 'F'

class DoubleBass(Strings):
    def __init__(self):
        super(Bass, self).__init__()


# Keyboards -----------------------------------------------------------

'''This includes a method to separate a single line or chord between staves.
Eventually, there should be an intelligent or user-defined split point.
It also should belong to a Keyboard superclass to spread the love.'''

class Piano(Voice):
    def __init__(self):
        super(Piano, self).__init__()
        self.inst_range = [(0, 9), (8, 0)]

    def make_part(self, time_signature: Time_Signature) -> Iterable[Part]:

        """divide notelist into two lists, divided by middle c"""

        note_list_bottom = []
        note_list_top = []

        for idx, note in enumerate(self.note_list):
            if idx < len(self.note_list) - 1:
                advance_note = self.note_list[idx + 1]
            if isinstance(note, Note) and isinstance(advance_note, Note):
                if advance_note.is_chord_member is True:
                    if note.octave >= 4:
                        note_list_top.append(note)
                    elif note.octave < 4:
                        note_list_bottom.append(note)
                    else:
                        raise Exception('Note is out of range.')
                elif advance_note.is_chord_member is False:
                    if note.octave >= 4:
                        note_list_top.append(note)
                        note_list_bottom.append(Rest(note.dur))
                    elif note.octave < 4:
                        note_list_bottom.append(note)
                        note_list_top.append(Rest(note.dur))
                    else:
                        raise Exception('Note is out of range.')

            elif isinstance(note, Note):

                if note.octave >= 4:
                    note_list_top.append(note)
                    note_list_bottom.append(Rest(note.dur))
                elif note.octave < 4:
                    note_list_bottom.append(note)
                    note_list_top.append(Rest(note.dur))
                else:
                    raise Exception('Note is out of range.')

            elif isinstance(note, Rest):
                note_list_top.append(note)
                note_list_bottom.append(note)

            else:
                raise Exception('Not a Note or Rest.')

        bottom = Part(note_list_bottom, time_signature)
        top = Part(note_list_top, time_signature)

        # for top_measure, bottom_measure in zip(top.measures, bottom.measures):
        #     for top_beat, bottom_beat in zip(top_measure.beats, bottom_measure.beats):
        #         for top_note, bottom_note in zip(top_beat.notes, bottom_note.notes):
        #             print('top:\t{}, bottom:\t{}'.format(top_note, bottom_note))

        """keep parts in score order"""
        self.part = [top, bottom]
        return self.part     
