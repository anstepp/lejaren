from lejaren.notation import Note

from lejaren.intake.import_musicxml import inputParser

class noteIntake:

    def __init__(self, parser=None, import_file=None):
        if not parser:
            self.parser = inputParser(import_file)
        else:
            self.parser = parser
        self.Note = None # define now; must create note later

    def _convert_to_note(self):
        pass