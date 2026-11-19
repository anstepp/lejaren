from lejaren.notation import Measure, Beat
from lejaren.log.log import get_logger

log = get_logger()

STANDARDDIVS = [
    (1, "whole"),
    (2, "half"),
    (4, "quarter"),
    (8, "eighth"),
    (16, "16th"),
    (32, "32nd"),
    (64, "64th"),
]

BEATTYPES = [
    "1024th",
    "512th",	
    "256th",	
    "128th",	
    "64th",	
    "32nd",	
    "16th",	
    "eighth",	
    "quarter",	
    "half",	
    "whole",	
    "breve",	
    "long",
    "maxima",
]

class Metronome:

    metronome_relation = "equal" #NB: ONLY OPTION

    def __init__(self, beat_unit, tempo):
        if not isinstance(beat_unit, str):
            log.debug("Inexact Beat Unit; guessing...")
            if beat_unit in STANDARDDIVS:
                pass
            else:
                #bail?
                log.debug("Can't make good guess, quarter is 60..")
                # set to boring, default q = 60
                self.beat_unit = "quarter"
                self.per_minute = 60 # prevent overwrite?
        else:
            if not any(beat_unit in row for row in BEATTYPES):
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
        
