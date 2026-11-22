from lejaren._types import TIME_SIGNATURE

import lejaren.log.log as logger
log = logger.get_logger()

def _test_for_low_bottom_time_sig(
        time_sig: TIME_SIGNATURE, measure_factor: int
) -> int:
    """
    Evaulates if TIME_SIGNATURE is valid or needs to be scaled.

    Arguments:
    ----------
    time_sig: a TIME_SIGNATURE

    measure_factor (int): a scaling factor for the measure (usually acquired internally).

    """
    if time_sig[1] < 3:
        log.debug("Setting measure factor to time sig by multiplication... < 3")
        new_measure_factor = measure_factor * time_sig[1]
        return new_measure_factor
    elif time_sig[1] > 4:
        log.debug("Setting measure factor to time sig by division... > 4")
        new_measure_factor = 4 / time_sig[1]
        return new_measure_factor
    else:
        return measure_factor