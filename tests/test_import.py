from collections import namedtuple

import pytest

from lejaren.intake.import_musicxml import inputParser

passing_files = [
                  "test.musicxml", 
                  "test.mxl", 
                  "test.xml",
                  ]

failing_files = [
                  "test.wav", 
                  "test.aif", 
                  "test.aiff",
                ]

def get_file_open(file_name): 
    assert inputParser(file_name)

def test_file_open():
    for test_file in passing_files:
        get_file_open(test_file)

@pytest.mark.xfail
def test_file_open_fail():
    for test_file in failing_files:
        get_file_open(test_file)

def test_file_conversion():
    pass