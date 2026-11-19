from typing import Final, List, Tuple

from lejaren._types import TIME_SIGNATURES, TIME_SIGNATURE

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