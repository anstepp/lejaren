import pytest

from lxml import etree

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

def test_convert_score_parts_to_xml(simple_score_with_singleton_sig, basic_iteration, tmp_path):
    xml_file = tmp_path / "default_test.xml"
    s = simple_score_with_singleton_sig
    assert s
    s.convert_to_xml(xml_file)
    assert xml_file.exists()
    tree = etree.parse(str(xml_file))
    root = tree.getroot()

    for idx, element in enumerate(root.iter()):
        assert element.tag == basic_iteration[idx]

def test_add_title(simple_score_with_singleton_sig, basic_iteration, tmp_path):
    xml_file = tmp_path / "default_test.xml"
    s = simple_score_with_singleton_sig
    assert s
    s.title = "Cool Title"
    s.convert_to_xml(xml_file)
    assert xml_file.exists()
    tree = etree.parse(str(xml_file))
    root = tree.getroot()

    temp_iteration = list(basic_iteration)
    temp_iteration.insert(1, "movement-title")
    basic_iteration = tuple(temp_iteration)

    for idx, element in enumerate(root.iter()):
        assert element.tag == basic_iteration[idx]
        if element.tag == "movement-title":
            assert element.text == "Cool Title"

def test_add_composer(simple_score_with_singleton_sig, basic_iteration, tmp_path):
    xml_file = tmp_path / "default_test.xml"
    s = simple_score_with_singleton_sig
    assert s
    s.composer = "Homer Simpson"
    s.convert_to_xml(xml_file)
    assert xml_file.exists()
    tree = etree.parse(str(xml_file))
    root = tree.getroot()

    temp_iteration = list(basic_iteration)
    temp_iteration.insert(1,"identification")
    temp_iteration.insert(2, "creator")
    basic_iteration = tuple(temp_iteration)

    for idx, element in enumerate(root.iter()):
        assert element.tag == basic_iteration[idx]
        if element.tag == "creator":
            assert element.text == "Homer Simpson"

def test__from_etree(simple_score_with_singleton_sig):
    s = simple_score_with_singleton_sig
    assert s