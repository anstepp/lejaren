import pytest

from lejaren.notation.score import Score
from lejaren.notation.part import Part
from lejaren.notation.note import Note
from lejaren.notation.rest import Rest

from lejaren.intake.import_notes import noteIntake

@pytest.fixture
def simple_score():
    note_list = [Note(4,4,0)]
    time_sig = [(4,4)]
    part = Part(note_list, time_sig)
    part_list = [part]
    return Score(part_list)

@pytest.fixture
def double_score():
    middle_c = Note(4,4,0)
    treble_staff_c = Note(4,5,0)
    note_list_one = [middle_c]
    note_list_two = [treble_staff_c]
    time_sig = [(4,4)]
    part_1 = Part(note_list_one, time_sig)
    part_2 = Part(note_list_two, time_sig)
    part_list = [part_1, part_2]
    return Score(part_list)

@pytest.fixture
def double_score_alt_rest():
    middle_c = Note(4,4,0)
    treble_staff_c = Note(4,5,0)
    full_rest = Rest(4)
    note_list_one = [middle_c, full_rest]
    note_list_two = [full_rest, treble_staff_c]
    time_sig = [(4,4)]
    part_1 = Part(note_list_one, time_sig)
    part_2 = Part(note_list_two, time_sig)
    part_list = [part_1, part_2]
    return Score(part_list)

def test_note_create(simple_score):
    assert noteIntake(simple_score)

def test_note_duration(simple_score, double_score):
    simple_intake = noteIntake(simple_score)
    assert simple_intake.parts[0]["staff_count"] == 1
    double_intake = noteIntake(double_score)
    print(double_intake.parts)
    assert double_intake.parts[0]["staff_count"] == 1
    assert double_intake.parts[1]["staff_count"] == 1


def test_note_pitch(simple_score, double_score, double_score_alt_rest):
    simple_intake = noteIntake(simple_score)
    assert isinstance(simple_intake.parts[0]['staves'][0], Part)
    for note in simple_intake.parts[0]['staves'][0].current_list:
        assert isinstance(note, Note)
        assert note == Note(4,4,0)
    double_intake = noteIntake(double_score)
    assert isinstance(double_intake.parts[0]['staves'][0], Part)
    assert isinstance(double_intake.parts[1]['staves'][0], Part)
    for note in double_intake.parts[0]['staves'][0].current_list:
        assert isinstance(note, Note)
        assert note == Note(4,4,0)
    for note in double_intake.parts[1]['staves'][0].current_list:
        assert isinstance(note, Note)
        assert note == Note(4,5,0)
        
    double_rest_intake = noteIntake(double_score_alt_rest)
    assert isinstance(double_rest_intake.parts[0]['staves'][0], Part)
    assert isinstance(double_rest_intake.parts[1]['staves'][0], Part)
    test_rest = Rest(4)
    test_rest.measure_toggle(False)
    print(test_rest)
    for idx, note in enumerate(double_rest_intake.parts[0]['staves'][0].current_list):
        if idx == 0:
            print("1", idx, note)
            assert isinstance(note, Note)
            assert note == Note(4,4,0)
        if idx == 1:
            print("1", idx, note)
            assert isinstance(note, Rest)
            assert note == test_rest
    for idx, note in enumerate(double_rest_intake.parts[1]['staves'][0].current_list):
        if idx == 0:
            print("2", idx, note)
            assert isinstance(note, Rest)
            assert note == test_rest
        if idx == 1:
            print("2", idx, note)
            assert isinstance(note, Note)
            assert note == Note(4,5,0)
    

def test_measure_mashing(double_score_alt_rest):
    pass

def test_set_ticks(simple_score):
    pass