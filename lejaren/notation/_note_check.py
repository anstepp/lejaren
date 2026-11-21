from lxml.etree import _Element

def _note_check(note: _Element) -> bool:
        # Use fall-through set to true; probably could be changed

        note_ok = False
        if (note.findall('.//duration') and note.findall('.//step') and note.findall('.//octave')):
            note_ok = True
        elif (len(note.findall('.//duration')) > 0 and len(note.findall('.//step')) > 0 and len(note.findall('.//octave'))) > 0:
            note_ok = True
        else:
            pass

        return note_ok