import pytest

from lejaren.notation import Chord, Note, Rest, Beat

def test_beat_creation():
    good_subdivisions = [1,2,3,4]
    for subdivisions in good_subdivisions:
        beat = Beat(subdivisions)
        assert beat

def test_beat_creation_bad():
    bad_subdivisions = ['str', True, 12.4]
    for subdivisions in bad_subdivisions:
        with pytest.raises(TypeError):
            beat = Beat(subdivisions)

def test_beams():
    beat = Beat(4)
    beam_condition = [(True, False, False), (False, True, True), (False, False, False)]
    test_notes = [Note(0.25,4,0), Note(0.25,4,1), Note(0.5,4,2)]
    for add_me in test_notes:
        beat.notes.append(add_me)
    beat.make_beams()
    for idx, note in enumerate(test_notes):
        assert beat.notes[idx] == note
    #start
    assert beat.notes[0].beam_start == True
    #continue
    assert beat.notes[1].beam_continue == True
    #end
    assert beat.notes[2].beam_end == True

def test_extend_beat():
    beat = Beat(4)
    test_notes = [Note(0.25,4,0), Note(0.25,4,1), Note(0.5,4,2)]
    beat.extend_beat(test_notes)
    for idx, note in enumerate(test_notes):
        assert beat.notes[idx] == note