# Hasami

Hasami is a tool to perform sentence segmentation on japanese text.

* In addition to simply splitting on sentence-ending markers like `！？。` 
  it will treat runs of sentence-ending characters as a single sentence ending.
* It will not split enclosed sentences, i.e. those in quotes or parentheses.
* It can be configured with custom sentence-ending markers and enclosures 
  in case the defaults don't cover your needs.
* You can define exceptions for when not to split sentences.

## Installation

```bash
pip install hasami
```

## Usage

A simple command line interface is provided to use the functionality
without having to write your own script. Input is read from `stdin` or from a file.
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

To use in your code: 

```python
import hasami

hasami.segment_sentences('これが最初の文。これは二番目の文。これが最後の文。')
# => ['これが最初の文。', 'これは二番目の文。', 'これが最後の文。']
```

*More complex examples will follow soon, please refer to the test cases in the meantime.* 

## License

Licensed under the BSD-3-Clause License