import pytest

import itertools

#Tempo Check Globals
# FIXME: Put insider larger fixture, so sharing is easier?
from lejaren.conversion.conversion_values import TicksForNotes, DefaultValues
tempos = [60, 72, 102, 120]
srs = [44100, 48000, 89000, 92000, 192000]

@pytest.fixture(scope="session")
def shared_output_dir(tmp_path_factory):
    # mktemp creates the actual directory structure
    base_dir = tmp_path_factory.mktemp("artifacts")
    return base_dir

@pytest.fixture
def sample_files(scope='function'):
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