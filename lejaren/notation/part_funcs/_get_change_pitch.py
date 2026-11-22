from lejaren.notation.measure import Measure

from ._get_index_range import _get_index_range

def _get_change_pitch(measures: list[Measure], index: int) -> list[Measure]:
    """
    Tests the change in pitch between measure starts in search range and
    weights the measure appropriately.

    Evaluates the differences in measure pitch between search index, ranking a pitch
    that is a local maxima higher and weighting the measure accordingly.

    Arguments:
    ----------

    index (int): index of measure to evaulate.

    Returns:
    --------

    None, measure ranking is held in measure object.
    """
    index_range_low, index_range_high = _get_index_range(index)
    test_measure_pitch = measures[index].beats[0]

    measure_range_to_weight = measures[index_range_low:index_range_high]

    if isinstance(index, int):
        # test downbeats
        for measure in measure_range_to_weight:
            if measure.beats[0] > test_measure_pitch:
                break
            else:
                measure.weight += 1
        for measure in measures:
            if measure.beats[0] < test_measure_pitch:
                break
            else:
                measure.weight += 1
    else:
        warnstr = f"Pitch index non-integer, was {type(index)}"
        log.warning(warnstr)
        raise TypeError(warnstr)

    return measure_range_to_weight
