import re

import pytest

from pathlib import Path

import xml.etree.ElementTree as ET

from lejaren.notation import Note, Part, Score, Chord

from tests.xml_order import XML_NOTE_ORDER, XML_MEASURE_ATTRIBUTE_ORDER

ORDER_TEST_FILE = "tests/test_files/simple_test_score_output.musicxml"

def increase_counter_and_return_truth(element, order, counter):
    max_count = (len(order) - 1)
    internal_counter = counter + 1
    if element.tag != order[internal_counter]:
        print(f"element: {element.tag}, order value: {order[internal_counter]}")
        if internal_counter < max_count:
            truth, counter = increase_counter_and_return_truth(element, order, internal_counter)
            return truth, counter
        else:
            truth = False
            return truth, counter
    else:
        truth = True
        return truth, counter


@pytest.fixture
def simple_test_note():
    test_middle_c = Note(4,4,0)
    return test_middle_c

@pytest.fixture
def simple_test_score(simple_test_note):
    time_signature = [(4,4)]
    simple_test_score = Score(Part([simple_test_note], time_signature))
    return simple_test_score

def test_xml_note_order():
    counter = 0
    order = XML_NOTE_ORDER
    assert Path.exists(ORDER_TEST_FILE)
    test_tree = ET.parse(ORDER_TEST_FILE)
    test_root = test_tree.getroot()
    note_element_to_test = test_root.find(".//measure/note")
    for element in note_element_to_test:
        truth, counter = increase_counter_and_return_truth(element, order, counter)
        assert truth
        

def test_xml_measure_attribute_order():
    counter = 0
    order = XML_MEASURE_ATTRIBUTE_ORDER
    assert Path.exists(ORDER_TEST_FILE)
    test_tree = ET.parse(ORDER_TEST_FILE)
    test_root = test_tree.getroot()
    measure_element_to_test = test_root.find(".//measure/attributes")
    for element in measure_element_to_test:
        truth, counter = increase_counter_and_return_truth(element, order, counter)
        assert truth


def test_xml_score_order(simple_test_score):
    assert simple_test_score