import unittest

import hasami.util


class TestUtil(unittest.TestCase):

    def test_make_enclosure_definitions(self):
        """Test that enclosure definitions can be generated from a string"""
        for enclosures, expected_definitions in [
            ('', []),
            ('「」', [('「', '」')]),
            ('（）「」『』', [('（', '）'), ('「', '」'), ('『', '』')])
        ]:
            with self.subTest(enclosures=enclosures):
                self.assertEqual(expected_definitions, hasami.util.make_enclosure_definitions(enclosures))

    def test_make_enclosure_definitions_requires_string_of_even_length(self):
        """Test that a string of even length is required"""
        with self.assertRaises(ValueError):
            hasami.util.make_enclosure_definitions('「」『')
