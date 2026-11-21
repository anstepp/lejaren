from lejaren._types import NOTE_LIST

import lejaren.log.log as logger
log = logger.get_logger()

def _join_ties(note_list: NOTE_LIST) -> list:
    tie_attr_list = ("tie_start", "tie_end", "tie_continue")
    for idx, note in enumerate(note_list):
        if any(hasattr(note, attr) for attr in tie_attr_list):
            #Verify adjacent notes tied
            if "tie_start":
                if hasattr(note[idx+1], "tie_continue"):
                    pass
                if hasattr(note[idx+1], "tie_end"):
                    pass
            if "tie_end":
                # This probably shouldn't happen! Test for it.
                log.warning("Check Tie End in Score _join_ties")
                pass
            if "tie_continue":
                # Might not be supposed to happen... test for it.
                log.warning("Check Tie Continue in _join_ties")
                pass