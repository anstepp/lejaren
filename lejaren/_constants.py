from typing import Final, List, Tuple

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

TIME_SIGNATURE: Final = Tuple[int, int]
TIME_SIGNATURES: Final = List[Tuple[int, int]]

MAX_LINES: Final[int] = 5
CLEFS: Final[Tuple[str]] = ["G", "C", "F"]