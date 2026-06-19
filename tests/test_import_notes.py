import pytest

from lejaren.intake.import_notes import noteIntake

@pytest.fixture
def sample_files(scope='function'):
    sample_files = [                  
                "test_files/test_treble_middle_c_full_score.musicxml",
                "test_files/test_treble_middle_c.mxl",       
                "test_files/test_treble_middle_c_full_score.mxl",
                "test_files/test_treble_middle_c.musicxml"
                ]
    return sample_files

def test_note_create(sample_files):
    for file in sample_files:
        assert noteIntake(import_file=file)


def test_note_duration():
    pass

def test_note_pitch():
    pass

def test_set_ticks():
    pass