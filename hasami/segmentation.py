import re
from typing import List, Union, Iterable, Pattern

import hasami.util

DEFAULT_SENTENCE_ENDING_MARKERS = '。！？!?‼⁈⁈⁇'

DEFAULT_ENCLOSURES = """〝〟「」『』（）〔〕［］｛｝｟｠〈〉《》【】〖〗〘〙〚〛‹›«»''""()[]{}｢｣"""


class Hasami:

    def __init__(
            self,
            sentence_ending_markers: str = DEFAULT_SENTENCE_ENDING_MARKERS,
            enclosures: str = DEFAULT_ENCLOSURES,
            exceptions: Iterable[Union[str, Pattern]] = ()
    ):
        """Construct an instance that recognizes the specified enclosures.

        :param enclosures: The enclosures that should be considered during segmentation.
        :param exceptions: Exceptions that should be considered during segmentation. Any newlines that
                           are matched by the specified patterns will be removed from the output.
        """

        # precompile all exceptions; re.compile() is idempotent so we can safely pass in already compiled patterns
        self.__exceptions = [re.compile(e) for e in exceptions]

        if not sentence_ending_markers:
            raise ValueError('At least one sentence-ending marker must be supplied')

        # The lookahead "(?!\n)" is used to avoid adding unnecessary
        # when there are already proper newlines in place.
        self.__sentence_ending_pattern = re.compile('([%s]+(?!\n))' % re.escape(sentence_ending_markers))

        # create regexp for all enclosures in the form of "『.?*』|「.?*」|..."
        # Since the matching is done by regex not all newlines that occur in nested enclosures of the same
        # kind, e.g. "「foo「!」bar!」" will be removed correctly due to the inability to match arbitrarily
        # nested balanced delimiters via regex. But this should not be a major problem, as natural text
        # will in general not contain such constructions very often.
        enclosure_def = hasami.util.make_enclosure_definitions(enclosures)
        enclosure_regex = '|'.join('%s.*?%s' % tuple(map(re.escape, e)) for e in enclosure_def)

        # the DOTALL modifier is needed to also match newlines with ".*"
        enclosure_pattern = re.compile(enclosure_regex, re.DOTALL)

        # removing enclosed newlines can be treated as any other exception
        self.__exceptions.append(enclosure_pattern)

    def insert_newlines(self, text: str) -> str:
        """Adds newlines to every identified sentence ending in the supplied text."""
        text = self.__sentence_ending_pattern.sub(r'\1\n', text)

        # Since the text could now contain newlines in invalid places,
        # we have to post-process it to remove those invalid newlines.
        for e in self.__exceptions:
            text = re.sub(e, lambda m: m.group(0).replace('\n', ''), text)

        return text

    def segment_sentences(self, text: str, strip_whitespace=True) -> List[str]:
        # Trailing whitespace ends up as an individual chunk after splitting: "〇〇〇。 " -> ["〇〇〇。", " "]
        # So we strip surrounding whitespace from the whole input to avoid that if requested.
        text = text.strip() if strip_whitespace else text

        # Since str.splitlines() returns an empty list for the empty string we need to manually preserve the
        # expected behaviour of returning a singleton list for text that contains just a single sentence.
        if text == '':
            return ['']

        sentences = self.insert_newlines(text).splitlines()

        if strip_whitespace:
            return [s.strip() for s in sentences]
        else:
            return sentences
