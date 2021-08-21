import pytest

from py2musicxml.notation import Chord, Note, Rest


def test_chord_init():

    middle_c = Note(4, 4, 0)
    octave_up_c = Note(4, 5, 0)

    simple_octave = Chord([middle_c, octave_up_c])

    assert len(simple_octave.notes) == 2
    assert simple_octave.notes[0].dur == 4
    assert simple_octave.notes[0].octave == 4
    assert simple_octave.notes[0].pc == 0
    assert simple_octave.notes[0].is_chord_member == False
    assert simple_octave.notes[1].dur == 4
    assert simple_octave.notes[1].octave == 5
    assert simple_octave.notes[1].pc == 0
    assert simple_octave.notes[1].is_chord_member == True
    assert simple_octave.dur == 4


def test_chord_init_fail_with_rest():

    rest = Rest(4)
    middle_c = Note(4, 4, 0)

    with pytest.raises(ValueError) as e:
        failed_chord = Chord([rest, middle_c])


def test_chord_init_fail_with_diff_durs():

    whole_note_c = Note(4, 4, 0)
    half_note_d = Note(2, 4, 2)

    with pytest.raises(ValueError) as e:
        failed_chord = Chord([whole_note_c, half_note_d])


def test_notes_ascending():

    middle_c = Note(4, 4, 0)
    middle_d = Note(4, 4, 2)
    middle_e = Note(4, 4, 4)

    chord = Chord([middle_e, middle_d, middle_c])

    assert len(chord.notes) == 3

    for idx, note in enumerate(chord.notes):
        if idx > 0:
            assert note > chord.notes[idx - 1]

    assert chord.notes[0].dur == 4
    assert chord.notes[0].octave == 4
    assert chord.notes[0].pc == 0
    assert chord.notes[0].is_chord_member == False
    assert chord.notes[1].dur == 4
    assert chord.notes[1].octave == 4
    assert chord.notes[1].pc == 2
    assert chord.notes[1].is_chord_member == True
    assert chord.notes[2].dur == 4
    assert chord.notes[2].octave == 4
    assert chord.notes[2].pc == 4
    assert chord.notes[2].is_chord_member == True


def test_split():

    dur = 8

    c = Note(dur, 4, 0)
    e = Note(dur, 4, 4)
    g = Note(dur, 4, 7)

    c_major = Chord([c, e, g])

    old_chord, new_chord = c_major.split(4)

    assert old_chord.dur == 4
    assert new_chord.dur == 4

    old_chord, new_chord = c_major.split(3)

    assert old_chord.dur == 5
    assert new_chord.dur == 3
