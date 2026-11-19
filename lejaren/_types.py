from typing import Tuple, List, Union, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from lejaren.notation import Note, Rest, Chord


type TIME_SIGNATURE = Tuple[int, int]
type TIME_SIGNATURES = List[Tuple[int, int]]

type ALL_DURATIONS = Union[Note, Rest, Chord]
type NO_CHORDS = Union[Note, Rest]
type ONLY_PITCH = Union[Note, Chord]

type NOTE_LIST = Iterable[ALL_DURATIONS]