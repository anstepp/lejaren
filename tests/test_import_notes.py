import pytest

from lejaren.notation.score import Score
from lejaren.notation.part import Part
from lejaren.notation.note import Note

from lejaren.intake.import_notes import noteIntake

@pytest.fixture
def score():
    return Score([Part([Note(4,4,0)], [(4,4)])])

def test_note_create(score: Score):
    assert noteIntake(score)


def test_note_duration():
    pass

def test_note_pitch():
    pass

def test_set_ticks():
    pass