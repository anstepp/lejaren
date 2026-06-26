from enum import Enum
from dataclasses import dataclass, field

from lejaren.notation import Note

class NOTE_VALUES(Enum): 
        WHOLE = 0
        HALF = 1
        QUARTER = 2
        QUARTER_T = 3 
        EIGHTH = 4
        EIGHTH_T = 5 
        SIXTEENTH = 6
        SIXTEENTH_T = 7

DEFAULT_AUDIO_SR = (44100, 48000, 89000, 96000, 128000)
DEFAULT_DIVISIONS = (4, 2, 1, .5, .25, .125)
DEFAULT_TRIPLETS = (.6666, .1666, 0.0833, 0.04166)

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