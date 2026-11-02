from pathlib import Path

import xml.etree.ElementTree as ET

from tests.xml_order import XML_NOTE_ORDER, XML_MEASURE_ATTRIBUTE_ORDER, XML_SCORE_ATTRIBUTE_ORDER

# TODO: more test files
ORDER_TEST_FILES = ["tests/test_files/simple_test_score_output.musicxml"]

def increase_counter_and_return_truth(element, order, counter):
    max_count = (len(order) - 1)
    internal_counter = counter + 1
    if not isinstance(element, str):
        element = element.tag
    else:
        if element != order[internal_counter]:
            print(f"element: {element}, order value: {order[internal_counter]}")
            if internal_counter < max_count:
                truth, counter = increase_counter_and_return_truth(element, order, internal_counter)
                return truth, counter
            else:
                truth = False
                return truth, counter
        else:
            truth = True
            return truth, counter

def test_xml_note_order():
    counter = 0
    order = XML_NOTE_ORDER
    for test_file in ORDER_TEST_FILES:
        assert Path.exists(test_file)
        test_tree = ET.parse(test_file)
        test_root = test_tree.getroot()
        note_element_to_test = test_root.find(".//measure/note")
        for element in note_element_to_test:
            truth, counter = increase_counter_and_return_truth(element.tag, order, counter)
            assert truth

def test_xml_measure_attribute_order():
    counter = 0
    order = XML_MEASURE_ATTRIBUTE_ORDER
    for test_file in ORDER_TEST_FILES:
        assert Path.exists(test_file)
        test_tree = ET.parse(test_file)
        test_root = test_tree.getroot()
        measure_element_to_test = test_root.find(".//measure/attributes")
        for element in measure_element_to_test:
            truth, counter = increase_counter_and_return_truth(element.tag, order, counter)
            assert truth

def test_xml_score_order():
    counter = 0
    order = XML_SCORE_ATTRIBUTE_ORDER
    for test_file in ORDER_TEST_FILES:
        assert Path.exists(test_file)
        test_tree = ET.parse(test_file)
        test_root = test_tree.getroot()
        score_types = XML_SCORE_ATTRIBUTE_ORDER[0]
        for scoretype in score_types:
            if test_root.tag == scoretype:
                score_element_to_test = test_root
            else:
                pass
        for element in score_element_to_test.attrib:
            truth, counter = increase_counter_and_return_truth(element, order, counter)
            assert truth