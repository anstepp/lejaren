import pytest

import itertools

from lejaren.conversion.conversion_values import TicksForNotes, DefaultValues

tempos = [60, 72, 102, 120]
srs = [44100, 48000, 89000, 92000, 192000]

@pytest.fixture(params=list(itertools.product(tempos, srs)))
def ticks(request):
    return TicksForNotes(request.param[0], request.param[1])

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