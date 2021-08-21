import pytest

from py2musicxml.notation import Note

TEST_DURATION, TEST_OCTAVE, TEST_PITCH_CLASS = 10, 8, 2


def test_object_init_fail_without_args():
    with pytest.raises(TypeError) as e:
        n = Note()


def test_object_init_success_with_args():
    n = Note(duration=TEST_DURATION, octave=TEST_OCTAVE, pitch_class=TEST_PITCH_CLASS)
    assert n.dur == TEST_DURATION
    assert n.octave == TEST_OCTAVE
    assert n.pc == TEST_PITCH_CLASS


def test_get_step_name():
    test_cases = {
        "no key": {
            "pitch_class": 2,
            "starting_pitch": 0,
            "expected_result": ["D", "0", "natural"],
        },
        "flat key": {
            "pitch_class": 6,
            "starting_pitch": 5,
            "expected_result": ["G", "-1", "flat"],
        },
        "sharp key": {
            "pitch_class": 9,
            "starting_pitch": 11,
            "expected_result": ["A", "0", "natural"],
        },
    }

    for test_case in test_cases.keys():
        n = Note(
            duration=TEST_DURATION,
            octave=TEST_OCTAVE,
            pitch_class=test_cases[test_case]["pitch_class"],
        )
        result = n._get_step_name(
            starting_pitch=test_cases[test_case]["starting_pitch"]
        )
        assert result == test_cases[test_case]["expected_result"]

    try:
        n = Note(
            duration=TEST_DURATION, octave=TEST_OCTAVE, pitch_class=TEST_PITCH_CLASS
        )
        n._get_step_name(starting_pitch=999)
    except Exception as e:
        assert str(e) == "starting_pitch must be zero, a flat key, or sharp key"


def test_note_equality():
    note_a = Note(duration=1, octave=2, pitch_class=3)
    note_b = Note(duration=1, octave=2, pitch_class=3)
    note_c = Note(duration=9, octave=8, pitch_class=7)

    assert note_a == note_b
    assert note_a != note_c


def test_articulations():

    note = Note(4, 4, 0)

    note.add_articulation("accent")

    assert note.articulation == "accent"

    with pytest.raises(ValueError):
        note.add_articulation("slur")


def test_ties():

    note = Note(4, 4, 0)
    note.add_articulation("accent")

    note.set_as_tie("tie_start")

    assert note.tie_start == True
    assert note.articulation == "accent"
    assert note.tie_continue == False
    assert note.tie_end == False

    note = Note(4, 4, 0)
    note.set_as_tie("tie_continue")

    assert note.tie_start == False
    assert note.tie_continue == True
    assert note.articulation is None
    assert note.tie_end == False

    note = Note(4, 4, 0)
    note.add_articulation("accent")
    note.set_as_tie("tie_end")

    assert note.tie_start == False
    assert note.tie_continue == False
    assert note.tie_end == True
    assert note.articulation is None


def test_split():

    dur = 8
    octave = 4
    pc = 0

    note_to_split = Note(dur, octave, pc)

    old_note, new_note = note_to_split.split(4)

    assert old_note.dur == 4
    assert old_note.octave == 4
    assert old_note.pc == 0
    assert new_note.dur == 4
    assert new_note.octave == 4
    assert new_note.pc == 0

    old_note, new_note = note_to_split.split(3)

    assert old_note.dur == 5
    assert old_note.octave == 4
    assert old_note.pc == 0
    assert new_note.dur == 3
    assert new_note.octave == 4
    assert new_note.pc == 0
