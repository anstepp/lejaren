from lejaren._types import PART_LIST
from lejaren._constants import EMPTY_MEASURE_FACTOR

from .rest import Rest
from .measure import Measure
from .beat import Beat

def _pad_with_empty_measures(parts: PART_LIST) -> int:
    """Returns score measure length (ie. max number of measures)"""

    max_len = 0

    # figure out which staff is the longest (largest number of measures)
    for part in parts:
        for staff in part["staves"]:
            if len(staff.measures) > max_len:
                max_len = len(staff.measures)
                longest_staff = staff

    for part in parts:
        for staff in part["staves"]:
            if len(staff.measures) < max_len:
                for idx in range(len(staff.measures), max_len):
                    ts = longest_staff.measures[idx].time_signature
                    measure_to_append = Measure(ts, EMPTY_MEASURE_FACTOR)

                    full_rest = ts[0]
                    empty_beat = Beat(ts[0])
                    empty_beat.add_note(Rest(full_rest))
                    measure_to_append.add_beat(empty_beat)
                    staff.measures.append(measure_to_append)

    return max_len