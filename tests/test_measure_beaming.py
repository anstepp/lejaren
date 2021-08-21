# NB: Because the Part object adds rests to cover an incomplete measure,
# write tests that are complete measures in this module.


import pytest
import copy

from py2musicxml.notation import Measure, Note, Rest

BASE_MEASURE_FACTOR = 4


def test_measure_whole_note():

    dur = 4

    middle_c = Note(dur, 4, 0)

    time_signature = (4, 4)

    m = Measure(time_signature, 1)

    m.add_note(middle_c)

    m.clean_up_measure()

    for beat in m.beats:
        assert beat.subdivisions == 1

        for note in beat.notes:
            assert note.dur == dur


def test_measure_quarter_note():

    dur = 1

    middle_c = Note(dur, 4, 0)

    time_signature = (4, 4)

    m = Measure(time_signature, 1)

    for n in [middle_c for x in range(4)]:
        m.add_note(n)

    m.clean_up_measure()

    for beat in m.beats:
        assert beat.subdivisions == 1

        for note in beat.notes:
            assert note.dur == dur


def test_eighth_note_beams():

    eighth_note_c = Note(0.5, 4, 0)

    time_sig = (4, 4)

    m = Measure(time_sig, 1)

    m.extend_measure([Note(0.5, 4, 0) for x in range(8)])

    m.clean_up_measure()

    counter = 0
    for beat in m.beats:
        counter += 1
        assert beat.subdivisions == 2
        assert len(beat.notes) == 2
        for idx, note in enumerate(beat.notes):
            assert note.dur == 1
            assert note.octave == 4
            assert note.pc == 0
            if idx % 2 == 0:
                assert note.beam_start
            else:
                pass

    assert len(m.beats) == m.time_signature[0]


def test_five_sixteenths():

    five_sixteenths_c = Note(1.25, 4, 0)
    remaining_rest = Rest(2.75)

    time_sig = (4, 4)
    measure_factor = 4

    m = Measure(time_sig, measure_factor)

    m.add_note(five_sixteenths_c)
    m.add_note(remaining_rest)

    m.clean_up_measure()

    assert m.beats[0].notes[0].dur == 4
    assert m.beats[1].notes[0].dur == 1


def test_half_note_multibeat():

    half_note_c = Note(2, 4, 0)
    remaining_rest = Rest(2)

    time_sig = (4, 4)

    m = Measure(time_sig, 1)

    m.add_note(half_note_c)
    m.add_note(remaining_rest)

    m.clean_up_measure()

    for beat in m.beats:
        assert beat.subdivisions == 1

    # assert m.beats[0].multi_beat == True
    assert m.beats[0].notes[0].dur == 2

    # assert m.beats[1].multi_beat == True
    assert m.beats[1].notes[0].dur == 2


def test_quarter_half_multibeat():

    quarter_note_c = Note(1, 4, 0)
    half_note_d = Note(2, 4, 2)
    remaining_rest = Rest(1)

    time_sig = (4, 4)
    measure_factor = 4

    m = Measure(time_sig, measure_factor)

    m.add_note(quarter_note_c)
    m.add_note(half_note_d)
    m.add_note(remaining_rest)

    m.clean_up_measure()

    for beat in m.beats:
        assert beat.subdivisions == 1

    assert len(m.beats) == 3

    # assert m.beats[0].multi_beat == False
    assert m.beats[0].notes[0].dur == 1
    assert m.beats[0].notes[0].pc == 0

    # assert m.beats[1].multi_beat == True
    assert m.beats[1].notes[0].dur == 2
    assert m.beats[1].notes[0].pc == 2

    # assert m.beats[2].multi_beat == False
    assert m.beats[2].notes[0].dur == 1
