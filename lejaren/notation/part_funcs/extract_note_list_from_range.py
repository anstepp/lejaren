from lejaren._types import NOTE_LIST

import lejaren.log.log as logger
log = logger.get_logger()

def extract_note_list_from_range(measures, min: int, max: int) -> NOTE_LIST:
    max_measures = len(measures)
    if not isinstance(min, int) and isinstance(max, int):
        warnstr = f"Ranges for note extraction not ints, were type: max: {max}, min: {min}"
        log.warning(warnstr)
        raise TypeError(warnstr)
    if min > max_measures or max > max_measures:
        warnstr = f"Values for min and/or max greater than measures: min: {min}, max: {max}, measure count: {max_measures}"
        log.warning(warnstr)
        raise ValueError(warnstr)
    if min > max:
        warnstr = f"Extration minimum measure is greater than maxiumum"
        log.warning(warnstr)
        raise ValueError(warnstr)
    else:
        note_list_to_crush = []
        note_list_to_return = []
        internal_list = measures[min:max]
        for measure in internal_list:
            for note in measure.notes:
                note_list_to_crush.append(note)
        note_list_to_return = note_list_to_crush
        for idx, note in enumerate(note_list_to_crush):
            note_to_append = note_list_to_crush[idx]
            if (idx + 1) < len(note_list_to_crush):
                if note_list_to_crush[idx] == note_list_to_crush[idx+1]:
                    note_to_append.dur += note_list_to_crush[idx+1].dur
                else:
                    note_list_to_return.append(note)
    return note_list_to_return