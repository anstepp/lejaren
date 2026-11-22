from itertools import cycle

from lejaren._types import TIME_SIGNATURES
from lejaren.notation.measure import Measure

def _make_new_measure(
    measures: list[Measure],
    time_signatures: TIME_SIGNATURES,
    current_measure: Measure,
    current_beat_count: int,
) -> Measure:

    time_sigs = cycle(time_signatures)

    next_ts = next(time_sigs)
    measure_max = next_ts[0]
    current_beat_count += next_ts[0]
    measures.append(current_measure)
    current_measure = Measure(next_ts, 1)

    return measures, current_measure, current_beat_count, measure_max