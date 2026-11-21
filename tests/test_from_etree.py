import pytest

from lxml import etree

from lejaren.notation import Score

@pytest.fixture
def basic_iteration():
    basic_iteration = (
            'score-partwise',
            'part-list',
            'score-part',
            'part-name',
            'part',
            'measure',
            'attributes',
            'divisions',
            'key',
            'fifths',
            'mode',
            'time',
            'beats',
            'beat-type',
            'staves',
            'clef',
            'sign',
            'line',
            'attributes',
            'divisions',
            'note',
            'pitch',
            'step',
            'alter',
            'octave',
            'duration',
            'accidental',
            'staff',
            'beam',
        )
    return basic_iteration

def test_from_etree(xml_file_list):
    for file in xml_file_list:
        s = Score(file)