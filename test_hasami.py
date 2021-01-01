import unittest

import hasami


class TestSentenceSegmentation(unittest.TestCase):

    def test_dont_modify_single_sentence(self):
        """Test that text without any (internal) sentence endings is left unmodified"""
        for text in ['', '。', '！', '？', 'これは単純な文です', 'これは単純な文です。', 'これは単純な文です！', 'これは単純な文です？', ]:
            with self.subTest(text=text):
                self.assertEqual([text], hasami.segment_sentences(text))

    def test_simple_segmentation(self):
        """Test that text is split on simple sentence endings"""
        for text, expected_sentences in [
            ('これが最初の文です。これは二番目の文です。これが最後の文です。', ['これが最初の文です。', 'これは二番目の文です。', 'これが最後の文です。']),
            ('これが最初の文です！これは二番目の文です！これが最後の文です！', ['これが最初の文です！', 'これは二番目の文です！', 'これが最後の文です！']),
            ('これが最初の文です？これは二番目の文です？これが最後の文です？', ['これが最初の文です？', 'これは二番目の文です？', 'これが最後の文です？'])
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

    @unittest.expectedFailure
    def test_nested_enclosures_not_segmented_correctly(self):
        """Document that text with nested enclosures of the same kind is currently not segmented correctly

        This is due to the fact that matching of enclosures is done by regex without any effort of trying to
        handle arbitrarily nested balanced delimiters. But this should not be a major problem, as natural text
        will in general not contain such constructions very often.
        """
        text = '外外外「〇〇〇「中中中。」〇〇〇！」外外外'
        self.assertEqual([text], hasami.segment_sentences(text))
