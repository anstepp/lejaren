from lejaren._types import NOTE_LIST, NO_CHORDS

from lejaren.notation.note import Note
from lejaren.notation.rest import Rest
from lejaren.notation.chord import Chord

def _flatten_chords(note_list: NOTE_LIST) -> NO_CHORDS:

    flat_list = []

    for idx, entry in enumerate(note_list):
        if isinstance(entry, (Note|Rest|Chord)):
            if type(entry) == Chord:
                flat_list.extend(entry.notes)
            else:
                flat_list.append(entry)
        else:
            raise TypeError(f"Non-note or Chord when trying to Flatten Chords, was {type(entry)}")

    return flat_list