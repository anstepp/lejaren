import pytest

from lejaren.conversion.conversion_values import TicksForNotes, DefaultValues

def test_creation(ticks):
    assert ticks
    assert isinstance(ticks, TicksForNotes)

def test_return_type(ticks):
    assert isinstance(ticks.get_tempo_ticks(), DefaultValues)

def test_return_tuple_ascending(ticks):
    return_tuple = ticks.get_tempo_ticks()
    previous_value = -1
    for sample_count in return_tuple.standard_ticks:
        assert sample_count > previous_value
        previous_value = sample_count