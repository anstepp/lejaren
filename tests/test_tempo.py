import pytest

from py2musicxml.notation import Tempo, Measure, Score

@pytest.fixture
def basic_tempo():
    bpm = 60
    note = 1 # quarter
    tempo = Tempo(bpm, note)
    return tempo, bpm, note

@pytest.fixture
def basic_score():
    time_sig = [(4,4)]
    measures = [m.Measure(time_sig, 1) for x in range(5)]
    test_part = Part(measures)
    test_score = Score([test_part])
    return test_score

def test_tempo_init(basic_tempo):
    tempo, bpm, note = basic_tempo
    assert tempo.tempo == bpm
    assert tempo.note_value == note

def test_set_tempo(basic_tempo):
    tempo, _, _ = basic_tempo
    new_bpm = 120
    new_note = 2 # half note
    tempo.set_tempo(new_bpm, new_note)
    assert tempo.tempo == new_bpm
    assert tempo.note_value == new_note

def test_stringify(basic_tempo):
    tempo, _, _ = basic_tempo
    assert f"{tempo}" == "Tempo:60, Beat:1, Samps@44100:735.0"

def test_samps_per_beat():

    # All these should have same samps/beat.
    # Default sampling rate is 44100.
    test_tempo_a = Tempo(60, 1)
    test_tempo_b = Tempo(120, 0.5)
    test_tempo_c = Tempo(30, 2)

    tempos = [test_tempo_a, test_tempo_b, test_tempo_c]

    for tempo in tempos:
        assert tempo.get_samps_per_beat() == 735
        assert tempo.get_samps_per_beat(sampling_rate=48000) == 800

    # Test dotted quarter
    test_tempo_d = Tempo(60, 1.5)
    assert test_tempo_d.get_samps_per_beat() == 490