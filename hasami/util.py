from typing import List, Tuple


def make_enclosure_definitions(enclosures: str) -> List[Tuple[str, str]]:
    """Creates enclosure definitions from a string of pairs of characters.

    Args:
        enclosures: A string of pairs of characters. Each pair of characters will be considered to
            signify the opening, resp. closing of an enclosure.

    Returns:
        A list of 2-tuples representing the opening and closing characters of an enclosure.
    """
    if len(enclosures) % 2 != 0:
        raise ValueError('Enclosures must be supplied as a string of even length')
    return [tuple(enclosures[i:i + 2]) for i in range(0, len(enclosures), 2)]
