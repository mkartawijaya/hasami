from typing import List

from hasami.segmentation import Hasami

DEFAULT_INSTANCE = Hasami()


def segment_sentences(text: str) -> List[str]:
    return DEFAULT_INSTANCE.segment_sentences(text)
