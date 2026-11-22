from fractions import Fraction
from math import gcd

from lejaren._types import TIME_SIGNATURES
from lejaren.notation.note import Note
from lejaren.notation.rest import Rest

def get_note_uniques(current_list: list) -> list:
    """
    Removes dupes of durs in list of Note objects.

    If a duration has yet to be listed, it appends it to the uniques. This is essential
    toward developing the factor, as note values are dependant upon being 1) integers,
    and 2) scaled to the time signature of the XML in MusicXML.

    Arguments:
    ----------

    None.

    Returns:
    --------

    uniques (list[int]): a list of unique durations in the current_list.


    """
    uniques = []
    for item in current_list:
        try:
            isinstance(item, (Note|Rest))
        except (TypeError, AttributeError):
            print(f"Non-Note in Part.get_note_uniques, is type {type(item)} instead")
        else:
            if item.dur not in uniques:
                uniques.append(item.dur)
    return uniques

def get_ts_uniques(time_signatures: TIME_SIGNATURES) -> TIME_SIGNATURES:
    """unique durations of the notes in the list"""
    uniques = []
    for item in time_signatures:
        if item[1] not in uniques:
            uniques.append(item[1])
        else:
            pass
    return uniques

def _get_factor(current_list, time_signatures) -> int:
    """
    Returns a factor (int) that scales all duration values to ints.

    Converts all durations to fractions, then finds the least common multiple. This is
    then returned as the factor to scale durations for MusicXML.

    Arguments:
    ----------

    input_list (list[float]): list of unique durations. (See _get_uniques).

    Returns:

    factor (int): scaling factor for MusicXML.

    """

    

    dur_uniques = get_note_uniques(current_list)
    denominator_uniques = get_ts_uniques(time_signatures)

    input_list = dur_uniques

    fractional_list = [
        Fraction(x).limit_denominator(128) for x in input_list
    ]
    denominators = [x.denominator for x in fractional_list]
    if denominators:
        lcm = denominators[0]
        for i in denominators[1:]:
            lcm = int(lcm * i / gcd(lcm, i))
        factor = lcm
    else:
        factor = 1

    return factor * max(denominator_uniques)
