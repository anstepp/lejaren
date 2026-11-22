from typing import Tuple

def _get_index_range(self, index: int, search_range: int) -> Tuple[int, int]:
    """
    Returns range for searching for hypermetric analysis.

    Not yet implemented. Cleans a search range for beginning and ends of a list.

    Arguments:
    ----------

    index (int): location of note to compare in measure list.

    search_range (int): adjacent measures on both sides
    """

    if isinstance(index, int) and isinstance(search_range, int):
        if index < search_range:
            return 0, search_range + index
        else:
            return index - search_range, index + search_range
    else:
        raise TypeError(f"Non-integer search indices and ranges for measures, types were... index: {type(index)}, range: {type(search_range)}")
