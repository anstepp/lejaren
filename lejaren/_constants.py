from typing import Final, List, Tuple
from enum import Enum

FLAT_KEYS: Final[List[int]] = [1, 3, 5, 8, 10]
SHARP_KEYS: Final[List[int]] = [2, 4, 6, 7, 9, 11]

ARTICULATIONS: Final[List[str]] = [
            "accent",
            "breath-mark",
            "caesura",
            "detached-legato",
            "doit",
            "falloff",
            "plop",
            "scoop",
            "spiccato",
            "staccatissimo",
            "staccato",
            "stress",
            "strong-accent",
            "tenuto",
            "unstress",
        ]

MAX_LINES: Final[int] = 5
CLEFS: Final[Tuple[str]] = ["G", "C", "F"]

DEFAULT_SAMPLING_RATE = 44100
STANDARD_SAMPLING_RATES: Final[Tuple[int]] = (32000, 41000, 48000, 64000, 82000, 92000, 192000)

BEAT_TYPES = [
    "1024th",
    "512th",	
    "256th",	
    "128th",	
    "64th",	
    "32nd",	
    "16th",	
    "eighth",	
    "quarter",	
    "half",	
    "whole",	
    "breve",	
    "long",
    "maxima",
]

STANDARD_DIVS = [
    (1, "whole"),
    (2, "half"),
    (4, "quarter"),
    (8, "eighth"),
    (16, "16th"),
    (32, "32nd"),
    (64, "64th"),
]

METER_DIVISION_TYPES = {2: "Duple", 3: "Triple", 4: "Quadruple"}

ARTICULATIONS = ["accent",
"strong-accent",
"staccato",
"tenuto",
"detached-legato",
"staccatissimo",
"spiccato",
"scoop",
"plop",
"doit",
"falloff",
"breath-mark",
"caesura",
"stress",
"unstress",
"soft-accent",
"other-articulation",]

DIATONIC = {
    "C":0,
    "D":2,
    "E":4,
    "F":5,
    "G":7,
    "A":9,
    "B":11
}

EMPTY_MEASURE_FACTOR = 1

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

CLOCKFACE = 12