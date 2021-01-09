import re
from typing import List

import hasami.util

DEFAULT_SENTENCE_ENDING_MARKERS = '。！？'

DEFAULT_ENCLOSURES = '「」『』（）'

SENTENCE_SEPARATOR = chr(30)  # non-printable record separator


class Hasami:

    def __init__(
            self,
            sentence_ending_markers: str = DEFAULT_SENTENCE_ENDING_MARKERS,
            enclosures: str = DEFAULT_ENCLOSURES
    ):
        """Construct an instance that recognizes the specified enclosures.

        :param enclosures: The enclosures that should be considered during segmentation.
        """

        if not sentence_ending_markers:
            raise ValueError('At least one sentence-ending marker must be supplied')

        enclosure_def = hasami.util.make_enclosure_definitions(enclosures)
        # create regexp for all enclosures in the form of "『.?*』|「.?*」|..."
        self.__enclosure_pattern = re.compile('|'.join('%s.*?%s' % tuple(map(re.escape, e)) for e in enclosure_def))
        self.__sentence_ending_pattern = re.compile('([%s]+)' % re.escape(sentence_ending_markers))

    def __mark_sentence_endings(self, text: str) -> str:
        """
        Adds the sentence separator character to all sentence endings which can then be later used to split the sentences.
        """
        return self.__sentence_ending_pattern.sub(r'\1' + SENTENCE_SEPARATOR, text)

    def __remove_enclosed_sentence_endings(self, text: str) -> str:
        """
        Removes the sentence separator character from all enclosed parts of the input string.
        """
        # Since the matching is done by regex not all separators that occur in nested enclosures of the same
        # kind, e.g. "「foo「!」bar!」" will be removed correctly due to the inability to match arbitrarily
        # nested balanced delimiters via regex. But this should not be a major problem, as natural text
        # will in general not contain such constructions very often.
        return self.__enclosure_pattern.sub(lambda m: m.group(0).replace(SENTENCE_SEPARATOR, ''), text)

    def segment_sentences(self, text: str, strip_whitespace=True) -> List[str]:
        # if not removed trailing whitespace ends up as an individual chunk after splitting
        text = text.strip() if strip_whitespace else text
        marked_text = self.__remove_enclosed_sentence_endings(self.__mark_sentence_endings(text))
        sentences = marked_text.rstrip(SENTENCE_SEPARATOR).split(SENTENCE_SEPARATOR)
        return [s.strip() for s in sentences] if strip_whitespace else sentences
