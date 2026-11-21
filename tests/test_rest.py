import pytest

from lejaren.notation import Rest


def test_init():

    rest = Rest(4)

    assert rest.dur == 4
    # assert rest.is_measure == True


def test_init_fail_on_negative():

    with pytest.raises(ValueError) as e:
        rest = Rest(0)

    with pytest.raises(ValueError) as e:
        rest = Rest(-9)

def test_toggle():

    rest = Rest(1)


    good_toggle_list = [True, False]

    for toggle in good_toggle_list:
        rest.measure_toggle(toggle)
        assert rest.is_measure == toggle

    bad_toggle_list = [123, "true", "False"]

    for toggle in bad_toggle_list:
        with pytest.raises(TypeError):
            rest.measure_toggle(toggle)

def test_split():

    rest_to_split = Rest(8)

    old_rest, new_rest = rest_to_split.split(4)

    assert old_rest.dur == 4
    assert new_rest.dur == 4

    old_rest, new_rest = rest_to_split.split(3)

    assert old_rest.dur == 5
    assert new_rest.dur == 3

def test_eq():
    assert Rest(4) == Rest(4)
    assert Rest(5) != Rest(4)