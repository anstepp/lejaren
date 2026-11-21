import lejaren.log.log as logger
log = logger.get_logger()

from typing import Iterable

from .part import Part

def _parse_parts(parts: Iterable[Part]) -> Iterable[Part]:

    parsed_parts = []

    # parts is a single Part object.
    if isinstance(parts, Part):
        parsed_parts = [{"staff_count": 1, "staves": [parts]}]

    # parts is a list.
    elif isinstance(parts, list):
        parsed_parts = []

        for p in parts:
            if isinstance(p, list):
                parsed_parts.append({"staff_count": len(p), "staves": p})
            else:
                parsed_parts.append({"staff_count": 1, "staves": [p]})

    else:
        warnstr = "Invalid parts argument supplied to Score."
        log.warning(warnstr)
        raise TypeError(warnstr)

    return parsed_parts