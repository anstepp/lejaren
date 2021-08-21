import pytest

from lxml import etree

from py2musicxml.notation import Note, Part, Score, Chord


def test_xml_valid():
    pass


def test_whole_note_chord_in_XML():

    middle_c = Note(4, 4, 0)
    middle_e = Note(4, 4, 4)
    middle_g = Note(4, 4, 7)

    middle_c_major = Chord([middle_c, middle_e, middle_g])
