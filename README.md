# Hasami

Hasami is a tool to perform sentence segmentation on japanese text. 

* Sentences are split on common sentence ending markers like `！？。`
* Enclosed sentence endings will not be split, i.e. those inside quotes or parentheses.
* Runs of sentence ending markers are treated as a single sentence ending.
* You can configure custom sentence ending markers and enclosures if the defaults don't cover your needs.
* You can define exceptions for when not to split sentences.

## Installation

```bash
$ pip install hasami
```

## Usage

A simple command line interface is provided. Input is read from `stdin` or from a file.
```bash
$ echo "これが最初の文。これは二番目の文。これが最後の文。" | tee input.txt | hasami
これが最初の文。
これは二番目の文。
これが最後の文。

$ hasami input.txt
これが最初の文。
これは二番目の文。
これが最後の文。
```

Usage in code: 

```python
import hasami

hasami.segment_sentences('これが最初の文。これは二番目の文。これが最後の文。')
# => ['これが最初の文。', 'これは二番目の文。', 'これが最後の文。']
```

More examples:

```python
import hasami

# Instead of splitting you can also just insert newlines.
hasami.insert_newlines('これが最初の文。これは二番目の文。これが最後の文。')
# => 'これが最初の文。\nこれは二番目の文。\nこれが最後の文。\n'

# Runs of sentence ending markers are treated as a single sentence ending.
hasami.segment_sentences('え、本当…！？嘘だろ…')
# => ['え、本当…！？', '嘘だろ…']

# Enclosed sentence endings are ignored.
hasami.segment_sentences('「うまく行くかな？」と思った。')
# => ['「うまく行くかな？」と思った。']
```

## Customization

The defaults should work for most of the punctuation found in natural
text but it is possible to define custom enclosures and sentence ending markers if necessary.
You can also define exceptions for when sentence segmentation should not happen,
for example in cases of untypical use of punctuation. 

```python
from hasami import Hasami, DEFAULT_ENCLOSURES, DEFAULT_SENTENCE_ENDING_MARKERS

# Pass a string of pairs of opening/closing characters to define custom enclosures.
with_custom_enclosures = Hasami(enclosures=DEFAULT_ENCLOSURES + '<>')
with_custom_enclosures.segment_sentences('<うまく行くかな？>と思った。')
# => ['<うまく行くかな？>と思った。']

# Pass an empty string if you want all enclosures to be ignored.
without_enclosures = Hasami(enclosures='')
without_enclosures.segment_sentences('「うまく行くかな？」と思った。')
# => ['「うまく行くかな？', '」と思った。']

# Pass a string of characters that should be considered as sentence ending markers.
with_custom_endings = Hasami(sentence_ending_markers=DEFAULT_SENTENCE_ENDING_MARKERS + '．，')
with_custom_endings.segment_sentences('これが最初の文．これは二番目の文，これが最後の文．')
# => ['これが最初の文．', 'これは二番目の文，', 'これが最後の文．']

# Pass a list of patterns to define exceptions where segmentation should not happen.
# Make sure to include the newline which should be removed in the pattern.
with_exceptions = Hasami(exceptions=['君の名は。\n'])
with_exceptions.segment_sentences('君の名は。見たことあるの？')
# => ['君の名は。見たことあるの？']
``` 

## License

Released under the BSD-3-Clause License