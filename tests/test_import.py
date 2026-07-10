from collections import namedtuple

import pytest

from lejaren.notation.score import Score

from lejaren.intake.import_musicxml import inputParser

@pytest.fixture
def parser():
    return inputParser()

@pytest.fixture
def passing_files():
    passing_files = [
                  "test.musicxml", 
                  "test.mxl", 
                  "test.xml",
                  ]
    return passing_files

@pytest.fixture
def failing_files():
    failing_files = [
                  "test.wav", 
                  "test.aif", 
                  "test.aiff",
                ]
    return failing_files

@pytest.fixture
def data_files():
        
    data_files = {

        "uncompressed_data_files": [
            "tests/test_files/test_treble_middle_c_full_score.musicxml",
            "tests/test_files/test_treble_middle_c.musicxml"
        ],

        "compressed_data_files": [
            None
        ]

    }

    return data_files

def test_file_open(parser: inputParser, passing_files: list[str]):
    for test_file in passing_files:
        assert parser.clean_input(test_file)


def test_file_open_fail(parser: inputParser, failing_files: list[str]):
    for file in failing_files:
        with pytest.raises(ValueError):
            assert parser.clean_input(file)

def test_file_conversion(parser: inputParser, data_files: dict):
    uncompressed = data_files["uncompressed_data_files"]
    for file in uncompressed:
        score = parser._create_tree(file)
        assert isinstance(score, Score)