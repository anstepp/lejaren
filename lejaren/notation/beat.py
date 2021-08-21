from typing import Iterable

from py2musicxml.notation import Note
import py2musicxml.log as logger

logging = logger.get_logger()


class Beat:
    def __init__(self, subdivisions: int) -> None:
        self.notes = []
        self.tuplet = False
        self.subdivisions = subdivisions
        self.multi_beat = False
        self.actual_notes = 0

    def make_beams(self) -> None:
        for location, note in enumerate(self.notes):
            if location == 0:
                note.beam_start = True
            elif location == len(self.notes):
                note.beam_end = True
            else:
                note.beam_continue = True

    def add_note(self, note: Note) -> None:
        logging.debug(f"Appending note: {note}")
        self.notes.append(note)

    def extend_beat(self, notes: Iterable[Note]) -> None:
        self.notes.extend(notes)

    #     self._tuplet_test()

    # def _tuplet_test(self):
    #     value = []
    #     for note in self.notes:
    #         value.append(note.dur)
    #     print(value)
    #     value_set = set(value)
    #     if self.subdivisions % 3 == 0:

    def __str__(self) -> str:
        return f"Beat{{Subdivisions: {self.subdivisions}, Notes: {len(self.notes)}}}"
