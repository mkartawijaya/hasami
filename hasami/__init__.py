from typing import List

from hasami.segmentation import Hasami

DEFAULT_INSTANCE = Hasami()


def insert_newlines(text: str) -> str:
    return DEFAULT_INSTANCE.insert_newlines(text)


def segment_sentences(text: str, strip_whitespace=True) -> List[str]:
    return DEFAULT_INSTANCE.segment_sentences(text, strip_whitespace)
