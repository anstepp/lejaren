import pytest

from lejaren.notation import Note

TEST_DURATION, TEST_OCTAVE, TEST_PITCH_CLASS = 10, 8, 2

var_list = (
    "dur",
    "octave",
    "pitch_class",
    "step_name",
    "alter",
    "accidental",
    "tie_start",
    "tie_continue",
    "tie_end",
    "tuplet_start",
    "tuplet_continue",
    "tuplet_end"
)

func_list = (

)

def test_vars_on_instantiation(simple_test_note):
    assert isinstance(simple_test_note, Note)
    for var in var_list:
        assert hasattr(simple_test_note, var)

def test_funcs_on_instantiation(simple_test_note):
    assert isinstance(simple_test_note, Note)
    for func in func_list:
        assert hasattr(simple_test_note, func)

def test_object_init_fail_without_args():
    with pytest.raises(TypeError) as e:
        n = Note()


def test_object_init_success_with_args():
    n = Note(dur=TEST_DURATION, octave=TEST_OCTAVE, pitch_class=TEST_PITCH_CLASS)
    assert n.dur == TEST_DURATION
    assert n.octave == TEST_OCTAVE
    assert n.pitch_class == TEST_PITCH_CLASS


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
            dur=TEST_DURATION,
            octave=TEST_OCTAVE,
            pitch_class=test_cases[test_case]["pitch_class"],
        )
        result = n._get_step_name(
            starting_pitch=test_cases[test_case]["starting_pitch"]
        )
        assert result == test_cases[test_case]["expected_result"]

    try:
        n = Note(
            dur=TEST_DURATION, octave=TEST_OCTAVE, pitch_class=TEST_PITCH_CLASS
        )
        n._get_step_name(starting_pitch=999)
    except Exception as e:
        assert str(e) == "starting_pitch must be zero, a flat key, or sharp key"


def test_note_equality():
    note_a = Note(dur=1, octave=2, pitch_class=3)
    note_b = Note(dur=1, octave=2, pitch_class=3)
    note_c = Note(dur=9, octave=8, pitch_class=7)

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
    pitch_class = 0

    note_to_split = Note(dur, octave, pitch_class)

    old_note, new_note = note_to_split.split(4)

    assert old_note.dur == 4
    assert old_note.octave == 4
    assert old_note.pitch_class == 0
    assert new_note.dur == 4
    assert new_note.octave == 4
    assert new_note.pitch_class == 0

    old_note, new_note = note_to_split.split(3)

    assert old_note.dur == 5
    assert old_note.octave == 4
    assert old_note.pitch_class == 0
    assert new_note.dur == 3
    assert new_note.octave == 4
    assert new_note.pitch_class == 0

def test_convert_to_rest():

    note_to_convert = Note(4,4,0)

    rest = note_to_convert.make_rest()

def test_stem_y_pos_raise_on_fail_dir():

    note_to_adjust_stem = Note(1,4,0) # Quarter!

    with pytest.raises(ValueError):
        note_to_adjust_stem.adj_stem_len("nonsense", 10)

def test_stem_y_pos_raise_on_fail_distance():

    note_to_adjust_stem = Note(1,4,0) # Quarter!

    with pytest.raises(TypeError):
        note_to_adjust_stem.adj_stem_len("up", "stupid")


def test_stem_y_pos_adj():

    note_to_adjust_stem = Note(1,4,0)

    note_to_adjust_stem.adj_stem_len("up", 10)

    assert note_to_adjust_stem.dur == 1
    assert note_to_adjust_stem.octave == 4
    assert note_to_adjust_stem.pitch_class == 0
    assert note_to_adjust_stem.stem_flag == True
    assert note_to_adjust_stem.stem_dir == "up" # will get lowercased
    assert note_to_adjust_stem.stem_y_pos == 10

    #test case correction also
    note_to_adjust_stem.adj_stem_len("Up", 10)
    assert note_to_adjust_stem.dur == 1
    assert note_to_adjust_stem.octave == 4
    assert note_to_adjust_stem.pitch_class == 0
    assert note_to_adjust_stem.stem_flag == True
    assert note_to_adjust_stem.stem_dir == "up" # will get lowercased
    assert note_to_adjust_stem.stem_y_pos == 10


def test_set_stem_to_vanish():

    note_to_disappear_stem = Note(1,4,0)

    note_to_disappear_stem.hide_stem()

    assert note_to_disappear_stem.dur == 1
    assert note_to_disappear_stem.octave == 4
    assert note_to_disappear_stem.pitch_class == 0
    assert note_to_disappear_stem.stem_flag == True
    assert note_to_disappear_stem.stem_dir == "up"
    assert note_to_disappear_stem.stem_y_pos == 0


def test_set_x_pos():

    note_to_shift = Note(4,4,0)

    note_to_shift.set_x_pos(10)

    assert note_to_shift.dur == 4
    assert note_to_shift.octave == 4
    assert note_to_shift.pitch_class == 0
    assert note_to_shift.x_pos == 10
