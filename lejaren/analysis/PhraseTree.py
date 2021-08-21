import Tree


class PhraseTree(Tree):
    def __init__(self):
        getNoteList = self.PhraseGenerator(theList)

    def PhraseGenerator(self, notelist):
        total = 0
        for item in notelist:
            if tieTest(item):
                total + item
                yield item

    def tieTest(self, note):
        if note.tie_continue is False and note.tie_end is False:
            return True
        else:
            return False

    def makeList(self):
        pass
