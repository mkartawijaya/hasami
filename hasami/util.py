from typing import List, Tuple


def make_enclosure_definitions(enclosures: str) -> List[Tuple[str, str]]:
    if len(enclosures) % 2 != 0:
        raise ValueError('Enclosures must be supplied as a string of even length')
    return [tuple(enclosures[i:i + 2]) for i in range(0, len(enclosures), 2)]
