import subprocess
import tempfile
import unittest

COMMON_SUBPROCESS_ARGS = {
    'timeout': 5,
    'stdout': subprocess.PIPE,
    'universal_newlines': True
}


class TestCommandLineInterface(unittest.TestCase):

    def test_simple_invocation(self):
        """Test simple execution: read from stdin, write to stdout"""
        process = subprocess.run(
            ['python3', '-m', 'hasami.cli'],
            **COMMON_SUBPROCESS_ARGS,
            input='これは単純な文です。\nこれが最初の文です。これは二番目の文です。これが最後の文です。',
        )

        self.assertEqual(0, process.returncode)
        self.assertEqual('これは単純な文です。\nこれが最初の文です。\nこれは二番目の文です。\nこれが最後の文です。\n', process.stdout)

    def test_reading_from_file(self):
        """Test reading input from file"""
        with tempfile.NamedTemporaryFile() as file:
            file.write('これは単純な文です。\nこれが最初の文です。これは二番目の文です。これが最後の文です。'.encode('utf-8'))
            file.flush()

            process = subprocess.run(
                ['python3', '-m', 'hasami.cli', file.name],
                **COMMON_SUBPROCESS_ARGS,
            )

            self.assertEqual(0, process.returncode)
            self.assertEqual('これは単純な文です。\nこれが最初の文です。\nこれは二番目の文です。\nこれが最後の文です。\n', process.stdout)
