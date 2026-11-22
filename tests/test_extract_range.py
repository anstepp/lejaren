import pytest

from lejaren.notation.note import Note
from lejaren.notation.part import Part

from lejaren.notation.part_funcs.extract_note_list_from_range import extract_note_list_from_range

def test_extract_range(simple_test_note, simple_test_part):
    extract = extract_note_list_from_range(simple_test_part.measures, 0,1)
    assert extract
    assert extract[0] == simple_test_note
    with pytest.raises(TypeError):
        extract_note_list_from_range(simple_test_part.measures,"dumb",10)
        extract_note_list_from_range(simple_test_part.measures,10,"dumb")
        extract_note_list_from_range(simple_test_part.measures,"dumb","dumb")
    with pytest.raises(ValueError):
        extract_note_list_from_range(simple_test_part.measures,4,10)
        extract_note_list_from_range(simple_test_part.measures,10,4)
    longer_example = Part([simple_test_note for x in range(10)], (4,4))
    extract = extract_note_list_from_range(longer_example.measures, 0,1)
    assert extract
    assert extract[0] == simple_test_note
    extract = extract_note_list_from_range(longer_example.measures, 0,2)
    assert extract
    assert extract[0] == Note(8,4,0)