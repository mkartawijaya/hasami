from typing import List, Tuple


def make_enclosure_definitions(enclosures: str) -> List[Tuple[str, str]]:
    if len(enclosures) % 2 != 0:
        raise ValueError('A string of even length must be supplied')
    return [tuple(enclosures[i:i + 2]) for i in range(0, len(enclosures), 2)]
