import pytest

from lejaren.notation import Chord, Note, Rest, Beat

@pytest.mark.xfail
def test_beat_creation():
    good_subdivisions = [1,2,3,4]
    for subdivisions in good_subdivisions:
        beat = Beat(subdivisions)
        assert beat
    bad_subdivisions = ['str', True, 12.4]
    for subdivisions in bad_subdivisions:
        with pytest.raises(TypeError):
            Beat(subdivisions)