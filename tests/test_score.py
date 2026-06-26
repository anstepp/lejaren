import pytest

from pathlib import Path

from lxml import etree

from lejaren.notation import Note, Part, Score, Chord

@pytest.fixture
def xml_file_list():
    file_list = [f'tests/test_files/{f.name}' for f in Path('tests/test_files').iterdir() if f.is_file()]
    file_list = [item for item in file_list if item != "tests/test_files/.DS_Store"]
    return file_list

def test_xml_valid():
    pass

def test_create_note_list_without_ties_on_xml_parse():
    pass

def test_whole_note_chord_in_XML():

    test_time_sig = [(4,4)]

    middle_c = Note(4, 4, 0)
    middle_e = Note(4, 4, 4)
    middle_g = Note(4, 4, 7)

    middle_c_major = Chord([middle_c, middle_e, middle_g])

    assert middle_c_major
    assert middle_c_major.dur == 4

    part_c = Part([middle_c], test_time_sig)
    part_e = Part([middle_e], test_time_sig)
    part_g = Part([middle_g], test_time_sig)
    part_chord = Part([middle_c_major], test_time_sig)

    part_list = [part_c, part_e, part_g, part_chord]

    for part in part_list:
        assert isinstance(part, Part)

    test_score = Score(part_list)
    assert isinstance(test_score, Score)

def test_xml_parser(xml_file_list):
    test_score_list = []
    for address in xml_file_list:
        with open(address, "rb") as xml_file:
            tree = etree.parse(xml_file)
            root = tree.getroot()
            score = Score(tree)
            test_score_list.append(score)
    for score in test_score_list:
        assert isinstance(score, Score)