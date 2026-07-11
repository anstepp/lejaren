from functools import reduce

from lejaren.notation import Note, Score, Rest, Part

from lejaren.intake.import_musicxml import inputParser

settings_dict = {
    "grace_note": False,
    "tuplet": False,
}

class noteIntake:

    def __init__(self, score: Score, crush=False, time_sig=[(4,4)]):
        self.score = score
        self.parts = score._parts
        if crush:
            self._crushed_staves = self._crush_staves(self.score, time_sig=time_sig)

    def _convert_to_note(self, note_list: list, settings: dict):
        for part in note_list:
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

    def _eliminate_measures(self, score: Score) -> list:
        pre_process_note_list = []
        note_list_list = []
        for part in score._parts:
            print(part)
            part_note_list = []
            for measure in part['staves'][0].measures:
                for note in measure.notes:
                    part_note_list.append(note)
            pre_process_note_list.append(part_note_list)
        for note_list in pre_process_note_list:
            crushed_note_list = []
            for idx, note in enumerate(note_list):
                if isinstance(note, Note):
                    if any(
                        (
                            note.tie_start, 
                            note.tie_continue, 
                            note.tie_end
                        )
                    ):
                        growing_note = note
                        if note.tie_start:
                            growing_note += note_list[note_idx]
                            next_note_tie = True
                            note_idx = idx
                            while(next_note_tie): 
                                note_idx += 1
                                if note_list[note_idx].tie_continue:
                                    pass
                                elif note_list[note_idx].tie_end:
                                    next_note_tie = False
                                else:
                                    ValueError("Next note Tie is unattached from previous note")
                            crushed_note_list.append(growing_note)
                elif isinstance(note, Rest):
                    crushed_note_list.append(note)
                else:
                    raise ValueError(f"Attempt to append non note/rest in _eliminate_measures, is type: {type(note)}")
            note_list_list.append(crushed_note_list)
        return note_list_list

    def _crush_staves(self, score: Score, time_sig) -> Score:
        part_lists_no_measures = self._eliminate_measures(score)
        part_list = []
        beat_counter = 0
        for part in part_lists_no_measures:
            part_list.append(Part(part, time_sig))
        crushed_score = Score(part_list)
        return crushed_score