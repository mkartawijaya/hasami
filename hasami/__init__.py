import re

ENCLOSURES = ('「」', '『』', '（）')

# create regexp for all enclosures in the form of "『.?*』|「.?*」|..."
ENCLOSURE_PATTERN = re.compile('|'.join('%s.*?%s' % tuple(re.escape(c) for c in s) for s in ENCLOSURES))

SENTENCE_ENDING_PATTERN = re.compile(r'([。！？]+)')
SENTENCE_SEPARATOR = chr(30)  # non-printable record separator


def mark_sentence_endings(text):
    """
    Adds the SENTENCE_SEPARATOR character to all sentence endings which can then be later used to split the sentences.
    """
    return SENTENCE_ENDING_PATTERN.sub(r'\1' + SENTENCE_SEPARATOR, text)


def remove_enclosed_sentence_endings(text):
    """
    Removes the SENTENCE_SEPARATOR character from all enclosed parts of the input string.
    """
    # FIXME:
    # Due to the way the regexp is constructed this method is unable to correctly remove
    # all separators that occur in nested enclosures of the same kind, e.g. "「foo「!」bar!」".
    # But maybe this is not a major problem, as natural text will in general not contain
    # such constructions very often?
    return ENCLOSURE_PATTERN.sub(lambda m: m.group(0).replace(SENTENCE_SEPARATOR, ''), text)


def segment_sentences(text):
    marked_text = remove_enclosed_sentence_endings(mark_sentence_endings(text))
    return marked_text.rstrip(SENTENCE_SEPARATOR).split(SENTENCE_SEPARATOR)
