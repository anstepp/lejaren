from lejaren.log.log import get_logger

from lejaren._constants import STANDARD_DIVS, BEAT_TYPES

log = get_logger()

class Metronome:

    metronome_relation = "equal" #NB: ONLY OPTION

    def __init__(self, beat_unit, tempo):
        if not isinstance(beat_unit, str):
            log.debug("Inexact Beat Unit; guessing...")
            if beat_unit in STANDARD_DIVS:
                pass
            else:
                #bail?
                log.debug("Can't make good guess, quarter is 60..")
                # set to boring, default q = 60
                self.beat_unit = "quarter"
                self.per_minute = 60 # prevent overwrite?
        else:
            if not any(beat_unit in row for row in BEAT_TYPES):
                warnstr = f"Beat Unit isn't a note, is: {beat_unit}, type: {type(beat_unit)}"
                log.warning(warnstr)
                raise ValueError(warnstr)
            else:
                self.beat_unit = beat_unit
                self.dots = 0
                self.beat_unit_tied = 0
    
        if not isinstance(tempo, (int, float)):
            warnstr = f"Tempo must be int for float (numeric), was {type(tempo)}"
            log.warning(warnstr)
            raise TypeError(warnstr)
        else:
            self.per_minute = tempo

        #TODO: Maybe don't let these change?
        self.metronome_arrows = False
        self.metronome_note = False
        
