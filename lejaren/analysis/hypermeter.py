from lejaren.notation.measure import Measure
from lejaren.notation.part import Part

class Hypermeasure(Measure):

    def __init__(self):
        self.hyperpart = Part

    def _assign_measure_weight(self):
            """
            Assign weight for hypermetric ranking.
    
            Assigns a weight to the measure based on rules. Not yet implemented.
    
            Arguments:
            ----------
    
            None.
    
            Returns:
            --------
    
            None.
            """
            weight = 0
            for index, measure in enumerate(self.measures):
                self._get_change_pitch(10)
    
    def _compare_weight(self):
        pass
    