import pytest

from lejaren.notation.metronome import Metronome

def test_creation():
    m = Metronome("quarter", 60)
    assert m
    assert m.beat_unit == 'quarter'
    assert m.per_minute == 60

    m2 = Metronome(4, 60)
    assert m2
    assert m2.beat_unit == "quarter"
    assert m2.per_minute == 60

def test_creation_fail():
    with pytest.raises(ValueError):
        m = Metronome("bad string", 60)