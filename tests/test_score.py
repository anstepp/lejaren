import pytest

from lxml import etree

from lejaren.notation import Note, Part, Score, Chord


def test_xml_valid():
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