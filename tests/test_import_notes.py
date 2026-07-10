import pytest

from lejaren.intake.import_notes import noteIntake

def test_note_create(sample_files):
    for file in sample_files:
        assert noteIntake(import_file=file)


def test_note_duration():
    pass

def test_note_pitch():
    pass

def test_set_ticks():
    pass