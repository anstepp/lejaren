import pytest

from py2musicxml.notation import Measure, Note


def test_object_init_fail_without_args():
    with pytest.raises(TypeError) as e:
        m = Measure()


def test_object_init_success_with_args():
    time_sig = (4, 4)

    m = Measure(time_sig, 1)

    assert m.time_signature == time_sig
    assert m.is_empty() == True


@pytest.mark.parametrize(
    "time_signature, expected_meter_division, expected_meter_type, expected_meter_map",
    [
        ((4, 4), "Quadruple", "Simple", [1, 1, 1, 1]),
        ((3, 4), "Triple", "Simple", [1, 1, 1]),
        ((2, 4), "Duple", "Simple", [1, 1]),
        ((12, 8), "Quadruple", "Compound", [1.5, 1.5, 1.5, 1.5]),
        ((3, 8), "Triple", "Simple", [1, 1, 1]),
        ((2, 16), "Duple", "Simple", [1, 1]),
        ((6, 8), "Duple", "Compound", [1.5, 1.5]),
    ],
)
def test_create_measure_map(
    time_signature, expected_meter_division, expected_meter_type, expected_meter_map
):
    m = Measure(time_signature, 1)

    assert m.meter_division == expected_meter_division
    assert m.meter_type == expected_meter_type
    assert m.measure_map == expected_meter_map


@pytest.mark.parametrize(
    "time_signature, expected_cumulative_beats, expected_total_cumulative_beats",
    [
        # fmt: off
        ((4, 4), [1, 2, 3, 4], 4),
        ((3, 4), [1, 2, 3], 3),
        ((2, 4), [1, 2], 2),
        ((12, 8), [1.5, 3, 4.5, 6], 6),
        ((3, 8), [1, 2, 3], 3),
        ((2, 16), [1, 2], 2),
        ((6, 8), [1.5, 3], 3),
        # fmt: on
    ],
)
def test_cumulative_beats(
    time_signature, expected_cumulative_beats, expected_total_cumulative_beats
):
    m = Measure(time_signature, 1)

    assert m.cumulative_beats == expected_cumulative_beats
    assert m.total_cumulative_beats == expected_total_cumulative_beats


def test_rest_padding():

    short_note = Note(3, 4, 0)

    m = Measure((4, 4), 1)

    m.add_note(short_note)

    m.clean_up_measure()

    assert len(m.beats) == 2
    assert m.beats[0].notes[0].dur == 3
    assert m.beats[1].notes[0].dur == 1


def test_additive_meter_five_eight():

    time_signature = (5, 8)

    m = Measure(time_signature, 1)

    assert m.meter_type == "Additive"
    assert m.measure_map == [3, 2]


def test_additive_meter_seven_eight():

    time_signature = (7, 8)

    m = Measure(time_signature, 1)

    assert m.meter_type == "Additive"
    assert m.measure_map == [3, 2, 2]


# def test_additive_meter_eight_eight():

#     time_signature = (8, 8)

#     m = Measure(time_signature, 1)

#     assert m.meter_type == "Additive"
#     assert m.measure_map == [3, 3, 2]
