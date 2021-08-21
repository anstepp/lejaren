import pytest

from py2musicxml.notation import Measure, Note, Beat, Part, Score, Rest, Chord

# fmt: off
fj_pitches = [0, 2, 4, 0, 0, 2, 4, 0, 4, 5, 7, 4, 5, 7, 7, 9, 7, 5, 4, 0, 7, 9, 7, 5, 4, 0, 0, -5, 0, 0, -5, 0]
fj_durs = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 4, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 4, 2, 2, 4]
# fmt: on


@pytest.fixture
def notes_that_cause_duration_split():

    test_note_a = Note(4, 4, 4)
    test_note_b = Note(3, 3, 3)
    test_note_c = Note(6, 6, 6)
    test_rest = Rest(1)

    test_sig = [[3, 4]]
    test_list = [
        test_note_b,
        test_note_a,
        test_note_b,
        test_note_c,
        test_note_a,
        test_rest,
    ]

    return test_list, test_sig


def test_measure_equals_note():

    test_note = Note(4, 4, 0)

    time_sig = [(4, 4)]

    test_part = Part([test_note], time_sig)

    assert len(test_part.measures) == 1

    for measure_idx, measure in enumerate(test_part.measures):
        for beat_idx, beat in enumerate(measure.beats):
            for note_idx, note in enumerate(beat.notes):
                if isinstance(note, Note):
                    assert note.dur == 4
                    assert note.octave == 4
                    assert note.pc == 0


def test_note_less_than_measure():

    dur = 3
    octave = 4
    pc = 0

    measure_factor = 4

    test_note = Note(dur, octave, pc)

    time_sig = [(4, 4)]

    test_part = Part([test_note], time_sig)

    assert len(test_part.measures[0].beats) == 2

    assert test_part.measures[0].beats[0].notes[0].dur == dur
    assert test_part.measures[0].beats[0].notes[0].octave == octave
    assert test_part.measures[0].beats[0].notes[0].pc == 0

    assert test_part.measures[0].beats[1].notes[0].dur == 1
    assert test_part.measures[0].beats[1].notes[0].is_measure == False


def test_note_greater_than_measure():

    dur = 5
    octave = 4
    pc = 0

    test_note = Note(dur, octave, pc)

    time_sig = [(4, 4)]

    test_part = Part([test_note], time_sig)

    assert len(test_part.measures[0].beats) == 1
    assert len(test_part.measures[1].beats) == 2

    assert test_part.measures[0].beats[0].notes[0].dur == 4
    assert test_part.measures[0].beats[0].notes[0].octave == octave
    assert test_part.measures[0].beats[0].notes[0].pc == pc

    assert test_part.measures[1].beats[0].notes[0].dur == 1
    assert test_part.measures[1].beats[0].notes[0].octave == octave
    assert test_part.measures[1].beats[0].notes[0].pc == pc


def test_note_exactly_multiple_measures():

    dur = 8
    octave = 4
    pc = 0

    test_note = Note(dur, octave, pc)

    time_sig = [(4, 4)]

    test_part = Part([test_note], time_sig)

    assert test_part.measures[0].beats[0].notes[0].dur == 4
    assert test_part.measures[0].beats[0].notes[0].octave == 4
    assert test_part.measures[0].beats[0].notes[0].pc == 0

    assert test_part.measures[1].beats[0].notes[0].dur == 4
    assert test_part.measures[1].beats[0].notes[0].octave == 4
    assert test_part.measures[1].beats[0].notes[0].pc == 0


def test_greater_than_multiple_measures():
    dur = 9
    octave = 4
    pc = 0

    test_note = Note(dur, octave, pc)

    time_sig = [(4, 4)]

    test_part = Part([test_note], time_sig)

    assert test_part.measures[0].beats[0].notes[0].dur == 4
    assert test_part.measures[0].beats[0].notes[0].octave == 4
    assert test_part.measures[0].beats[0].notes[0].pc == 0

    assert test_part.measures[1].beats[0].notes[0].dur == 4
    assert test_part.measures[1].beats[0].notes[0].octave == 4
    assert test_part.measures[1].beats[0].notes[0].pc == 0

    assert test_part.measures[2].beats[0].notes[0].dur == 1
    assert test_part.measures[2].beats[0].notes[0].octave == 4
    assert test_part.measures[2].beats[0].notes[0].pc == 0


def test_two_notes_equal_two_measures():

    middle_c = Note(4, 4, 0)
    middle_d = Note(4, 4, 2)

    test_note_list = [middle_c, middle_d]

    time_sig = [(4, 4)]

    test_part = Part(test_note_list, time_sig)

    assert test_part.measures[0].beats[0].notes[0].dur == 4
    assert test_part.measures[0].beats[0].notes[0].octave == 4
    assert test_part.measures[0].beats[0].notes[0].pc == 0

    assert test_part.measures[1].beats[0].notes[0].dur == 4
    assert test_part.measures[1].beats[0].notes[0].octave == 4
    assert test_part.measures[1].beats[0].notes[0].pc == 2


def test_two_notes_equal_one_measure():

    middle_c = Note(2, 4, 0)
    middle_d = Note(2, 4, 2)

    test_note_list = [middle_c, middle_d]

    time_sig = [(4, 4)]

    test_part = Part(test_note_list, time_sig)

    assert test_part.measures[0].beats[0].notes[0].dur == 2
    assert test_part.measures[0].beats[0].notes[0].octave == 4
    assert test_part.measures[0].beats[0].notes[0].pc == 0

    assert test_part.measures[0].beats[1].notes[0].dur == 2
    assert test_part.measures[0].beats[1].notes[0].octave == 4
    assert test_part.measures[0].beats[1].notes[0].pc == 2


def test_two_notes_less_than_measure():

    middle_c = Note(2, 4, 0)
    middle_d = Note(1, 4, 2)

    test_note_list = [middle_c, middle_d]

    time_sig = [(4, 4)]

    test_part = Part(test_note_list, time_sig)

    assert test_part.measures[0].beats[0].notes[0].dur == 2
    assert test_part.measures[0].beats[0].notes[0].octave == 4
    assert test_part.measures[0].beats[0].notes[0].pc == 0

    assert test_part.measures[0].beats[1].notes[0].dur == 1
    assert test_part.measures[0].beats[1].notes[0].octave == 4
    assert test_part.measures[0].beats[1].notes[0].pc == 2


def test_two_notes_greater_than_one_measure():

    middle_c = Note(3, 4, 0)
    middle_d = Note(3, 4, 2)

    test_note_list = [middle_c, middle_d]

    time_sig = [(4, 4)]

    test_part = Part(test_note_list, time_sig)

    assert test_part.measures[0].beats[0].notes[0].dur == 3
    assert test_part.measures[0].beats[0].notes[0].octave == 4
    assert test_part.measures[0].beats[0].notes[0].pc == 0

    assert test_part.measures[0].beats[1].notes[0].dur == 1
    assert test_part.measures[0].beats[1].notes[0].octave == 4
    assert test_part.measures[0].beats[1].notes[0].pc == 2

    assert test_part.measures[1].beats[0].notes[0].dur == 2
    assert test_part.measures[1].beats[0].notes[0].octave == 4
    assert test_part.measures[1].beats[0].notes[0].pc == 2


def test_two_notes_one_greater_than_measure_one_less():

    middle_c = Note(9, 4, 0)
    middle_d = Note(2, 4, 2)

    test_note_list = [middle_c, middle_d]

    time_sig = [(4, 4)]

    test_part = Part(test_note_list, time_sig)

    assert test_part.measures[0].beats[0].notes[0].dur == 4
    assert test_part.measures[0].beats[0].notes[0].octave == 4
    assert test_part.measures[0].beats[0].notes[0].pc == 0

    assert test_part.measures[1].beats[0].notes[0].dur == 4
    assert test_part.measures[1].beats[0].notes[0].octave == 4
    assert test_part.measures[1].beats[0].notes[0].pc == 0

    assert test_part.measures[2].beats[0].notes[0].dur == 1
    assert test_part.measures[2].beats[0].notes[0].octave == 4
    assert test_part.measures[2].beats[0].notes[0].pc == 0

    assert test_part.measures[2].beats[1].notes[0].dur == 2
    assert test_part.measures[2].beats[1].notes[0].octave == 4
    assert test_part.measures[2].beats[1].notes[0].pc == 2


def test_measure_init_on_four_quarters():

    four_quarters = [Note(1, 4, 0) for x in range(4)]

    time_sig = [(4, 4)]

    test_part = Part(four_quarters, time_sig)

    assert len(test_part.measures) == 1
    assert len(test_part.measures[0].notes) == 4
    assert len(test_part.measures[0].beats) == 4
    assert len(test_part.measures[0].beats[0].notes) == 1
    for measure in test_part.measures:
        for beat in measure.beats:
            for note in beat.notes:
                assert note.dur == 1
                assert note.pc == 0
                assert note.octave == 4


def test_three_measure_overflow_change_time_sig():

    long_note = Note(9, 4, 0)

    time_sig = [(3, 4), (2, 4), (4, 4)]

    test_part = Part([long_note], time_sig)

    assert test_part.measures[0].notes[0].dur == 3
    assert test_part.measures[1].notes[0].dur == 2
    assert test_part.measures[2].notes[0].dur == 4


def test_part_durations_are_correct(notes_that_cause_duration_split):

    test_list, test_sig = notes_that_cause_duration_split
    test_part = Part(test_list, test_sig)

    expected_note_durations = [3, 3, 1, 2, 1, 2, 3, 1, 2, 2, 1]
    expected_note_pitches = [3, 4, 4, 3, 3, 6, 6, 6, 4, 4, None]
    # expected_beat_lens = [1, 1, 2, 2, 1, 2, 2, 1]

    note_count = 0

    for measure_idx, measure in enumerate(test_part.measures):
        for beat_idx, beat in enumerate(measure.beats):
            for note_idx, note in enumerate(beat.notes):

                expected_note_duration = expected_note_durations[note_count]
                expected_note_pitch = expected_note_pitches[note_count]

                assert note.dur == expected_note_duration

                if isinstance(note, Note):
                    # assert note.pc == expected_note_pitch
                    pass
                note_count += 1


def test_assert_unique(notes_that_cause_duration_split):

    test_list, test_sig = notes_that_cause_duration_split
    test_part = Part(test_list, test_sig)

    for index_x, x in enumerate(test_part.measures):
        # print(index_x)
        for index_y, y in enumerate(test_part.measures):
            if x is not y:
                # print(index_y, y, y.beats)
                assert not set(y.beats).intersection(set(x.beats))
            else:
                assert set(y.beats).intersection(set(x.beats)) == set(y.beats).union(
                    set(x.beats)
                )


def test_long_durs():
    # fmt: off
    long_durs = [4,4,4,4,7,1,4,6,7,3,8,6,7,1,5,6,1]
    long_durs_corrected = [4 * dur for dur in long_durs]
    long_durs_after_break = [4,4,4,4,4,3,1,4,4,2,2,4,1,3,4,4,4,2,2,4,1,1,2,3,1,4,1,1,2]
    long_durs_after_break_corr = [4 * dur for dur in long_durs_after_break]
    # fmt: on

    long_durs_list = [Note(x, 4, x) for x in long_durs]
    long_durs_part = Part(long_durs_list, [(4, 4)])

    long_durs_part_halved_list = [Note(x * 0.5, 4, x) for x in long_durs]

    note_count = 0
    for index, measure in enumerate(long_durs_part.measures):
        for beat in measure.beats:
            for note in beat.notes:
                expected_note_duration = long_durs_after_break[note_count]
                # print(note_count, note.dur, expected_note_duration)
                assert note.dur == expected_note_duration
                note_count += 1

    long_durs_score = Score(parts=[long_durs_part])
    long_durs_score.convert_to_xml("test_score_long.xml")


def test_frere_jacques():

    fj_ts = [[4, 4]]
    fj_list = [Note(dur, 4, pitch) for dur, pitch in zip(fj_durs, fj_pitches)]

    fj_part = Part(fj_list, fj_ts)

    counter = 0
    for measure_index, measure in enumerate(fj_part.measures):
        for beat_index, beat in enumerate(measure.beats):
            for note_index, note in enumerate(beat.notes):
                # print(counter, fj_durs[counter], note.dur)
                assert note.dur == fj_durs[counter]
                counter += 1

    score = Score(parts=[fj_part])
    score.convert_to_xml("test_score_fj.musicxml")


def test_fj_three_four():

    # fmt: off
    fj_durs_34 = [2,1,1,2,2,1,1,2,2,1,1,2,2,1,3,2,1,1,2,2,1,1,1,1,2,1,1,1,1,1,1,1,1,2,2,1,1,2,2,1,1,2,3,1,2]
    fj_durs_34_corrected = [dur * 4 for dur in fj_durs_34]
    # fmt: on
    fj_ts = [[3, 4]]
    fj_list = [Note(dur, 4, pitch) for dur, pitch in zip(fj_durs, fj_pitches)]

    fj_part = Part(fj_list, fj_ts)

    counter = 0
    for measure_index, measure in enumerate(fj_part.measures):
        for beat_index, beat in enumerate(measure.beats):
            for note_index, note in enumerate(beat.notes):
                # print(counter, fj_durs_34[counter], note.dur)
                assert note.dur * fj_durs_34[counter]
                counter += 1

    score = Score(parts=[fj_part])
    score.convert_to_xml("test_score_fj_34.musicxml")


def test_fj_shifting_ts():
    # fmt: off
    fj_durs_shift = [2,2,2,1,1,1,1,2,1,1,2,2,2,2,2,1,1,1,1,3,1,1,1,1,1,2,2,1,1,1,1,1,1,2,1,1,2,2,2,2,2,1,2,1,3]
    # fmt: on
    fj_ts = [(4, 4), (3, 4), (2, 4)]
    fj_list = [Note(dur, 4, pitch) for dur, pitch in zip(fj_durs, fj_pitches)]

    fj_part = Part(fj_list, fj_ts)

    score = Score(parts=[fj_part])
    score.convert_to_xml("test_score_fj_shifting.musicxml")

    counter = 0
    for measure_index, measure in enumerate(fj_part.measures):
        for beat_index, beat in enumerate(measure.beats):
            for note_index, note in enumerate(beat.notes):
                #print(measure_index, fj_durs_shift[counter], note, measure.time_signature)
                assert note.dur == fj_durs_shift[counter]
                counter += 1


def test_frere_jacques_subdiv():

    fj_ts = [[4, 4]]
    fj_list = [Note(dur, 4, pitch) for dur, pitch in zip(fj_durs, fj_pitches)]

    fj_part = Part(fj_list, fj_ts)

    fj_durs_halved = [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        2,
        1,
        1,
        2,
        0.5,
        0.5,
        0.5,
        0.5,
        1,
        1,
        0.5,
        0.5,
        0.5,
        0.5,
        1,
        1,
        1,
        1,
        2,
        1,
        1,
        2,
    ]
    fj_halved_list = [
        Note(dur, 4, pitch) for dur, pitch in zip(fj_durs_halved, fj_pitches)
    ]
    fj_halved_part = Part(fj_halved_list, fj_ts)

    fj_durs_quartered = [
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        1,
        0.5,
        0.5,
        1,
        0.25,
        0.25,
        0.25,
        0.25,
        0.5,
        0.5,
        0.25,
        0.25,
        0.25,
        0.25,
        0.5,
        0.5,
        0.5,
        0.5,
        1,
        0.5,
        0.5,
        1,
    ]
    fj_quartered_list = [
        Note(dur, 4, pitch) for dur, pitch in zip(fj_durs_quartered, fj_pitches)
    ]
    fj_quartered_part = Part(fj_quartered_list, fj_ts)

    assert fj_halved_part.measure_factor == 8
    assert fj_quartered_part.measure_factor == 16

    counter = 0
    for measure_index, measure in enumerate(fj_part.measures):
        for beat_index, beat in enumerate(measure.beats):
            for note_index, note in enumerate(beat.notes):
                #print(counter, fj_durs[counter], note.dur)
                assert note.dur == fj_durs[counter]
                counter += 1

    score = Score(parts=[fj_part, fj_halved_part, fj_quartered_part])
    score.convert_to_xml("test_score_fj_subdiv.xml")

    score_two = Score(parts=[fj_quartered_part])
    score_two.convert_to_xml("test_score_fj_only_quarter.musicxml")


def test_chord_parsed():

    c = Note(4, 4, 0)
    e = Note(4, 4, 4)
    g = Note(4, 4, 7)

    c_major = Chord([c, e, g])

    ts = [(4, 4)]

    test_chord_part = Part([c_major], ts)

    assert len(test_chord_part.measures[0].beats) == 1
    assert test_chord_part.measures[0].beats[0].notes[0].notes[0].dur == 4
    assert test_chord_part.measures[0].beats[0].notes[0].notes[1].dur == 4
    assert test_chord_part.measures[0].beats[0].notes[0].notes[2].dur == 4


def test_chord_split_simple():

    c = Note(8, 4, 0)
    e = Note(8, 4, 4)
    g = Note(8, 4, 7)

    c_major = Chord([c, e, g])

    ts = [(4, 4)]

def test_chord_parsed():

    c = Note(4,4,0)
    e = Note(4,4,4)
    g = Note(4,4,7)

    c_major = Chord([c,e,g])

    ts = [(4,4)]

    test_chord_part = Part([c_major], ts)

    # assert len(test_chord_part.measures[0].beats) == 1
    # assert test_chord_part.measures[0].beats[0].notes[0].dur == 4
    # assert test_chord_part.measures[0].beats[0].notes[1].dur == 4
    # assert test_chord_part.measures[0].beats[0].notes[2].dur == 4

def test_chord_split_simple():
    
    c = Note(8,4,0)
    e = Note(8,4,4)
    g = Note(8,4,7)

    c_major = Chord([c,e,g])

    ts = [(4,4)]

    test_chord_part = Part([c_major], ts)

    assert len(test_chord_part.measures[0].beats) == 1
    assert len(test_chord_part.measures[1].beats) == 1
