import copy
from typing import Tuple
from decimal import Decimal

import lejaren.log as logger

logging = logger.get_logger()


class Rest:
    def __init__(self, duration):
        self.dur = Decimal(str(self._check_duration(duration)))
        self.is_measure = False

    def _check_duration(self, duration: float) -> float:
        if duration <= 0:
            logging.error(f"Negative rest duration: {duration}")
            raise ValueError(f"Rest duration ({duration}) must be positive")
        else:
            return duration

    def change_duration(self, new_duration: float) -> None:
        self.dur = Decimal(str(self._check_duration(new_duration)))

    def measure_toggle(self, toggle: bool) -> None:
        self.is_measure = toggle

    def __str__(self):
        return "Duration: {}, is_measure {}".format(self.dur, self.is_measure)

    def split(self, diff) -> Tuple["__class__", "__class__"]:
        old_rest = copy.deepcopy(self)
        new_rest = copy.deepcopy(self)

        old_rest.dur = self.dur - diff
        new_rest.dur = diff
        return old_rest, new_rest

    def __eq__(self, other) -> bool:
            """
            Absolute equality test for two rests.

            Tests equality of duration, octave, and pitch class for two
            rests. Testing Rest == Rest is expected usage.

            Arguments:

            other (Rest): a rest to test equality.

            Returns:

            bool
            """

            if (
                (self.dur == other.dur)
            ):
                return True
            else:
                return False