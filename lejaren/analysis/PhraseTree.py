from lejaren._types import NOTE_LIST

import Tree

class PhraseTree(Tree):
    def __init__(self, note_list: NOTE_LIST):
        self.note_list = self.PhraseGenerator(note_list)

    def PhraseGenerator(self, note_list: NOTE_LIST):
        total = 0
        for item in note_list:
            if self.tieTest(item):
                total + item
                yield item

    def tieTest(self, note):
        if note.tie_continue is False and note.tie_end is False:
            return True
        else:
            return False

    def makeList(self):
        pass
