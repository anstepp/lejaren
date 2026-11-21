from dataclasses import dataclass, field

from lejaren._constants import DEFAULT_DIVISIONS, DEFAULT_TRIPLETS

@dataclass
class DefaultValues:
    tempo: int
    SR: int
    standard_ticks: dict = field(init=False)
    
    def __post_init__(self):
        self.standard_ticks = self._make_standard_subdivision_ticks(self.tempo, self.SR)
    
    def _make_standard_subdivision_ticks(self, tempo: int, SR: int) -> dict:
        if tempo == None and SR == None:
            # TODO: Warn on empty values for logging
            raise ValueError(f"No tempo or SR")

        ticks = self._get_ticks(tempo, SR)
        unordered_divisions = []

        for div in DEFAULT_DIVISIONS:
            # TODO: Warn on cast to int with decmial value
            unordered_divisions.append(int(ticks*div))
        for div in DEFAULT_TRIPLETS:
            # TODO: Warn on cast to int with decimal value
            unordered_divisions.append(int(ticks*div))

        ordered_divisons = tuple(sorted(unordered_divisions))

        return ordered_divisons
    
    def _get_ticks(self, tempo, SR):
        return (SR * 60) / tempo
    
class TicksForNotes:

    def __init__(self, tempo: int, SR: int):
        self.tempo_ticks = DefaultValues(tempo, SR)

    def get_tempo_ticks(self):
        return self.tempo_ticks