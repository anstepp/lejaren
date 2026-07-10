from lejaren.notation import Note

from lejaren.intake.import_musicxml import inputParser

settings_dict = {
    "grace_note": False,
    "tuplet": False,
}

class noteIntake:

    def __init__(self, score):
        self.score = score

    def _convert_to_note(self, settings: dict):
        for part in self.Score:
            for note in part:
                for setting in settings:
                    try:
                        if setting == True:
                            setting += "_toggle_on"
                            getattr(note, setting)()
                        else:
                            setting += "_toggle_off"
                            getattr(note, setting)()
                    except:
                        AttributeError(f"Note does not have attribute {setting}")
                    print(note)