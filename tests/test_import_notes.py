import pytest

from lejaren.notation.score import Score
from lejaren.notation.part import Part
from lejaren.notation.note import Note

from lejaren.intake.import_notes import noteIntake

@pytest.fixture
def score():
    return Score([Part([Note(4,4,0)], [(4,4)])])

def test_note_create(score):
    assert noteIntake(score)

def test_note_duration(score):
    intake = noteIntake(score)
    assert intake.parts[0]["staff_count"] == 1

def test_note_pitch(score):
    intake = noteIntake(score)
    assert isinstance(intake.parts[0]['staves'][0], Part)
    for note in intake.parts[0]['staves'][0].current_list:
        assert isinstance(note, Note)
        assert note == Note(4,4,0)

def test_set_ticks(score):
    pass