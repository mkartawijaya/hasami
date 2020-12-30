from unittest import TestCase

import hasami


class TestSentenceSegmentation(TestCase):
    def test_no_modification_single_sentence(self):
        text = 'これは単純な文です。'
        self.assertEqual([text], hasami.segment_sentences(text))

    def test_simple_segmentation(self):
        self.assertEqual([
            'これが最初の文です。',
            'これは二番目の文です。',
            'これが最後の文です。'
        ], hasami.segment_sentences('これが最初の文です。これは二番目の文です。これが最後の文です。'))

        self.assertEqual([
            'これが最初の文です！',
            'これは二番目の文です！',
            'これが最後の文です！'
        ], hasami.segment_sentences('これが最初の文です！これは二番目の文です！これが最後の文です！'))

        self.assertEqual([
            'これが最初の文です？',
            'これは二番目の文です？',
            'これが最後の文です？'
        ], hasami.segment_sentences('これが最初の文です？これは二番目の文です？これが最後の文です？'))

    def test_segmentation_on_runs_of_sentence_ending_markers(self):
        self.assertEqual([
            'これが最初の文です！！！',
            'これは二番目の文です！？',
            'これが最後の文です。！？。？！'
        ], hasami.segment_sentences('これが最初の文です！！！これは二番目の文です！？これが最後の文です。！？。？！'))

    def test_enclosed_sentence_ending_is_ignored(self):
        self.assertEqual([
            'これが最初の文です。',
            '「これは二番目の文です。」これが最後の文です。',
        ], hasami.segment_sentences('これが最初の文です。「これは二番目の文です。」これが最後の文です。'))

        self.assertEqual([
            'これが最初の文です。',
            '『これは二番目の文です。』これが最後の文です。',
        ], hasami.segment_sentences('これが最初の文です。『これは二番目の文です。』これが最後の文です。'))

        self.assertEqual([
            'これが最初の文です。',
            '（これは二番目の文です。）これが最後の文です。',
        ], hasami.segment_sentences('これが最初の文です。（これは二番目の文です。）これが最後の文です。'))
