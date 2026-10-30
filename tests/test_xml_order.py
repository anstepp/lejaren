import re

import pytest

from pathlib import Path

from lxml import etree

from lejaren.notation import Note, Part, Score, Chord

@pytest.fixture
def simple_test_note():
    test_middle_c = Note(4,4,0)
    return test_middle_c

@pytest.fixture
def simple_test_score(simple_test_note):
    time_signature = [(4,4)]
    simple_test_score = Score(Part([simple_test_note], time_signature))
    return simple_test_score


def test_xml_note_order(simple_test_note):
    assert simple_test_note

def test_xml_measure_attribute_order():
    pass

def test_xml_score_order(simple_test_score):
    assert simple_test_score