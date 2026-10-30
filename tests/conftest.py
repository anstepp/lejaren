import pytest

import itertools

from lejaren.notation import Score, Part, Note, Rest, Chord

#Tempo Check Globals
# FIXME: Put insider larger fixture, so sharing is easier?
from lejaren.conversion.conversion_values import TicksForNotes, DefaultValues
tempos = [60, 72, 102, 120]
srs = [44100, 48000, 89000, 92000, 192000]

@pytest.fixture(scope="session")
def shared_output_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("output")

@pytest.fixture(scope='function')
def sample_files():
    sample_files = [                  
                "test_files/test_treble_middle_c_full_score.musicxml",
                "test_files/test_treble_middle_c.mxl",       
                "test_files/test_treble_middle_c_full_score.mxl",
                "test_files/test_treble_middle_c.musicxml"
                ]
    return sample_files

@pytest.fixture(params=list(itertools.product(tempos, srs)))
def ticks(request):
    return TicksForNotes(request.param[0], request.param[1])

@pytest.fixture
def simple_test_note():
    test_middle_c = Note(4,4,0)
    return test_middle_c

@pytest.fixture
def single_time_sig():
    time_signature = (4,4)
    return time_signature

@pytest.fixture
def list_time_sig():
    time_signature = [(4,4)]
    return time_signature

@pytest.fixture
def simple_test_score(simple_test_note):
    time_signature = [(4,4)]
    simple_test_score = Score(Part([simple_test_note], time_signature))
    return simple_test_score

@pytest.fixture
def score_with_list_sig(simple_test_note, list_time_sig):
    simple_test_score = Score(Part([simple_test_note], list_time_sig))
    return simple_test_score

@pytest.fixture
def simple_score_with_singleton_sig(simple_test_note, single_time_sig):
    simple_test_score = Score(Part([simple_test_note], single_time_sig))
    return simple_test_score