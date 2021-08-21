from __future__ import annotations

from itertools import cycle, compress
from typing import Iterable

CLOCKFACE = 12


class PitchClassSet:
    def __init__(self, pcs: Iterable[int]) -> None:

        self.ordered_set = [x for x in set(pcs) if x is not None]

        self.ordered_list = list(self.ordered_set)

        self.ordered_list.sort()

        self.cardinality = len(self.ordered_list)

        self.normal_order = self._get_normal_order(self.ordered_list)

    def _get_normal_order(self, pclist: Iterable[int]) -> Iterable[int]:

        cycled_set = cycle(pclist)

        potential_set_orders = []

        for set_start in range(self.cardinality):

            current_set = []

            for current_pc in range(self.cardinality):

                next_cycled_set = next(cycled_set)
                current_set.append(next_cycled_set)

            zeroed_set = self._get_zero_start(current_set)
            zeroed_set_reversed = self._retrograde_TI(zeroed_set)

            potential_set_orders.append(zeroed_set)

            if zeroed_set != zeroed_set_reversed:

                potential_set_orders.append(zeroed_set_reversed)

            next(cycled_set)

        first_to_last_pc_distance = [
            (s[-1] - s[0]) % CLOCKFACE for s in potential_set_orders
        ]

        minimum_distance = min(first_to_last_pc_distance)

        compression_mask = [
            1 if dist == minimum_distance else 0 for dist in first_to_last_pc_distance
        ]

        minimum_distance_list = list(
            compress(first_to_last_pc_distance, compression_mask)
        )

        candidates = []

        for idx, value in enumerate(compression_mask):
            if value == 1:
                minimum_potential = potential_set_orders[idx]
                candidates.append(minimum_potential)

        candidates = self._remove_list_dupes(candidates)

        smallest_intervals = self._get_smallest_intervals_sorted(candidates)

        return smallest_intervals

    def _remove_list_dupes(self, candidates: Iterable[int]) -> Iterable[int]:

        no_duplicates = []

        for candidate in candidates:
            if candidate not in no_duplicates:
                no_duplicates.append(candidate)

        return no_duplicates

    def _get_zero_start(self, pcs: Iterable[int]) -> Iterable[int]:
        zero_set = [(x - pcs[0]) % CLOCKFACE for x in pcs]

        return zero_set

    def _get_smallest_intervals_sorted(
        self, candidates: Iterable[list]
    ) -> Iterable[int]:

        generators = [self._interval_generator(candidate) for candidate in candidates]

        for idx in range(self.cardinality):
            current_intervals = [next(g) for g in generators]
            minimum_interval = min(current_intervals)
            counter = 0
            for interval in current_intervals:
                if interval == minimum_interval:
                    counter += 1
            if counter == 1:
                for interval, candidate in zip(current_intervals, candidates):
                    if interval == minimum_interval:

                        return candidate

    def _interval_generator(self, candidate: Iterable[int]):

        last_pc = 0

        for pc in candidate:
            interval = last_pc + pc
            last_pc = pc
            yield interval

    def _retrograde(self, reverse_me: Iterable[int]) -> Iterable[int]:
        reversed_list = reverse_me.reverse()

        return reversed_list

    def _retrograde_TI(self, reverse_me: Iterable[int]) -> Iterable[int]:
        reversed_list = []

        for var in reverse_me[::-1]:
            if var == 0:
                var = CLOCKFACE

            tied = ((CLOCKFACE - var) + reverse_me[-1]) % CLOCKFACE

            reversed_list.append(tied)

        return reversed_list

    def transpose(self, interval: int) -> PitchClassSet:

        new_pcs = [(pc + interval) % CLOCKFACE for pc in self.ordered_list]

        return PitchClassSet(new_pcs)

    def invert(self) -> PitchClassSet:

        new_pcs = [(CLOCKFACE - pc) % CLOCKFACE for pc in self.ordered_list]

        return PitchClassSet(new_pcs)

    def transpositional_inversion(self, interval: int) -> PitchClassSet:

        new_pcs = [
            ((CLOCKFACE - pc) + interval) % CLOCKFACE for pc in self.ordered_list
        ]

        return PitchClassSet(new_pcs)

    def get_compliment(self) -> PitchClassSet:

        new_pcs = [x for x in range(CLOCKFACE) if x not in self.ordered_list]

        return PitchClassSet(new_pcs)
