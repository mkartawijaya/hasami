import re
import unittest

import hasami
from hasami.util import make_enclosure_definitions


class TestSentenceSegmentation(unittest.TestCase):

    def test_dont_modify_single_sentence(self):
        """Test that text without any (internal) sentence endings is left unmodified"""
        for text in ['', '。', '！', '？', 'これは単純な文です', 'これは単純な文です。', 'これは単純な文です！', 'これは単純な文です？']:
            with self.subTest(text=text):
                self.assertEqual([text], hasami.segment_sentences(text))

    def test_insert_newlines(self):
        """Test that newlines are added to sentence endings"""
        for text, expected_sentences in [
            ('これは単純な文です', 'これは単純な文です'),
            ('これは単純な文です。', 'これは単純な文です。\n'),
            ('これが最初の文です。これは二番目の文です。これが最後の文です。', 'これが最初の文です。\nこれは二番目の文です。\nこれが最後の文です。\n'),
            ('これが最初の文です。「これは二番目の文です。」これが最後の文です。', 'これが最初の文です。\n「これは二番目の文です。」これが最後の文です。\n'),
            ('これが最初の文です。   これは二番目の文です。   これが最後の文です。', 'これが最初の文です。\n   これは二番目の文です。\n   これが最後の文です。\n'),
            # inserting unnecessary newlines should be avoided
            ('これが最初の文です。\nこれは二番目の文です。\nこれが最後の文です。', 'これが最初の文です。\nこれは二番目の文です。\nこれが最後の文です。\n'),
        ]:
            with self.subTest(text=text):
                self.assertEqual(expected_sentences, hasami.insert_newlines(text))

    def test_simple_segmentation(self):
        """Test that text is split on simple sentence endings"""
        for text, expected_sentences in [
            ('これが最初の文です。これは二番目の文です。これが最後の文です。', ['これが最初の文です。', 'これは二番目の文です。', 'これが最後の文です。']),
            ('これが最初の文です！これは二番目の文です！これが最後の文です！', ['これが最初の文です！', 'これは二番目の文です！', 'これが最後の文です！']),
            ('これが最初の文です？これは二番目の文です？これが最後の文です？', ['これが最初の文です？', 'これは二番目の文です？', 'これが最後の文です？']),
            # inserting unnecessary newlines should be avoided
            ('これが最初の文です。\nこれは二番目の文です。\nこれが最後の文です。', ['これが最初の文です。', 'これは二番目の文です。', 'これが最後の文です。']),
        ]:
            with self.subTest(text=text):
                self.assertEqual(expected_sentences, hasami.segment_sentences(text))

    def test_runs_of_sentence_ending_markers(self):
        """Test that runs of multiple sentence ending markers are treated as a single sentence ending"""
        self.assertEqual([
            'これが最初の文です！！！',
            'これは二番目の文です！？',
            'これが最後の文です。！？。？！'
        ], hasami.segment_sentences('これが最初の文です！！！これは二番目の文です！？これが最後の文です。！？。？！'))

    def test_ignore_enclosed_sentence_endings(self):
        """Test that text is not split on enclosed sentence endings"""
        for text, expected_sentences in [
            ('「これは単純な文です。」', ['「これは単純な文です。」']),
            ('『これは単純な文です。』', ['『これは単純な文です。』']),
            ('（これは単純な文です。）', ['（これは単純な文です。）']),
            ('これが最初の文です。「これは二番目の文です。」これが最後の文です。', ['これが最初の文です。', '「これは二番目の文です。」これが最後の文です。']),
            ('これが最初の文です。『これは二番目の文です。』これが最後の文です。', ['これが最初の文です。', '『これは二番目の文です。』これが最後の文です。']),
            ('これが最初の文です。（これは二番目の文です。）これが最後の文です。', ['これが最初の文です。', '（これは二番目の文です。）これが最後の文です。']),
            ('外外外「中中中。」外外外『中中中。』外外外', ['外外外「中中中。」外外外『中中中。』外外外']),
            ('外外外（〇〇〇「中中中。」〇〇〇『中中中。』〇〇〇。）外外外', ['外外外（〇〇〇「中中中。」〇〇〇『中中中。』〇〇〇。）外外外']),
            # in case of overlap the first "complete" enclosure wins leaving the second one "open".
            ('外外外「中中中『〇〇〇。」中中中。』外外外', ['外外外「中中中『〇〇〇。」中中中。', '』外外外'])
        ]:
            with self.subTest(text=text):
                self.assertEqual(expected_sentences, hasami.segment_sentences(text))

    def test_strip_whitespace(self):
        """Test that surrounding whitespace is stripped from sentences by default"""
        for text, expected_sentences in [
            (' ', ['']),
            (' 。     ', ['。']),
            (' 〇〇〇。 〇〇〇。 〇〇〇。 ', ['〇〇〇。', '〇〇〇。', '〇〇〇。']),
        ]:
            with self.subTest(text=text):
                self.assertEqual(expected_sentences, hasami.segment_sentences(text))

    def test_keep_whitespace(self):
        """Test that surrounding whitespace can optionally be kept"""
        for text, expected_sentences in [
            (' ', [' ']),
            (' 。     ', [' 。', '     ']),
            (' 〇〇〇。 〇〇〇。 〇〇〇。 ', [' 〇〇〇。', ' 〇〇〇。', ' 〇〇〇。', ' ']),
        ]:
            with self.subTest(text=text):
                self.assertEqual(expected_sentences, hasami.segment_sentences(text, strip_whitespace=False))

    @unittest.expectedFailure
    def test_nested_enclosures_not_segmented_correctly(self):
        """Document that text with nested enclosures of the same kind is currently not segmented correctly

        This is due to the fact that matching of enclosures is done by regex without any effort of trying to
        handle arbitrarily nested balanced delimiters. But this should not be a major problem, as natural text
        will in general not contain such constructions very often.
        """
        text = '外外外「〇〇〇「中中中。」〇〇〇！」外外外'
        self.assertEqual([text], hasami.segment_sentences(text))

    def test_default_sentence_ending_markers(self):
        """Test that certain sentence ending markers are defined by default"""
        for marker in hasami.DEFAULT_SENTENCE_ENDING_MARKERS:
            with self.subTest(marker):
                text = 'これが最初の文です%sこれは二番目の文です。' % marker
                self.assertEqual([
                    'これが最初の文です%s' % marker,
                    'これは二番目の文です。'
                ], hasami.segment_sentences(text))

    def test_custom_sentence_ending_markers(self):
        """Test that custom sentence-ending markers can be defined"""
        instance = hasami.Hasami(sentence_ending_markers='.,')
        self.assertEqual([
            'これが最初の文です.',
            'これは二番目の文です,',
            'これが最後の文です。'
        ], instance.segment_sentences('これが最初の文です.これは二番目の文です,これが最後の文です。'))

    def test_sentence_ending_marker_required(self):
        """Test that at least one sentence-ending markers has to be defined"""
        with self.assertRaises(ValueError):
            hasami.Hasami(sentence_ending_markers='')

    def test_default_enclosures(self):
        """Test that certain enclosures are defined by default"""
        for opening, closing in make_enclosure_definitions(hasami.DEFAULT_ENCLOSURES):
            with self.subTest(opening + closing):
                text = '外外外%s中中中。%s外外外。' % (opening, closing)
                self.assertEqual([text], hasami.segment_sentences(text))

    def test_custom_enclosures(self):
        """Test that custom enclosures can be defined"""
        for enclosures, text, expected_sentences in [
            ('##$$', '「外外外#中中中。#外外外。$中中中。$外外外」', ['「外外外#中中中。#外外外。', '$中中中。$外外外」']),
            # if there are no enclosures defined then all sentence endings will be split
            ('', '外外外「中中中。」外外外『中中中。』外外外', ['外外外「中中中。', '」外外外『中中中。', '』外外外'])
        ]:
            with self.subTest(enclosures=enclosures):
                instance = hasami.Hasami(enclosures=enclosures)
                self.assertEqual(expected_sentences, instance.segment_sentences(text))

    def test_custom_exceptions(self):
        """Test that exceptions can be defined"""
        instance = hasami.Hasami(exceptions=[
            # ignore untypical use of punctuation
            '君の名は。\n',
            # remove internal/errant newlines
            r'\w\n\w',
            # remove empty lines
            re.compile(r'(?<=\n)\s+\n')
        ])

        for text, expected_sentences in [
            ('君の名は。見たことあるの', ['君の名は。見たことあるの']),
            ('これは\n単純な文\nです', ['これは単純な文です']),
            ('これが最初の文です。 \nこれは二番目の文です。 \nこれが最後の文です。', ['これが最初の文です。', 'これは二番目の文です。', 'これが最後の文です。'])
        ]:
            with self.subTest(text=text):
                self.assertEqual(expected_sentences, instance.segment_sentences(text))
