import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SKILL = Path(__file__).resolve().parents[1]
RUNTIME = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local/share')) / 'ai-english-checker'


@unittest.skipUnless((RUNTIME / 'venv/bin/python').exists(), 'Run scripts/install.sh first')
class LauncherTests(unittest.TestCase):
    def run_check(self, args=(), text=None, env=None):
        return subprocess.run(
            ['bash', str(SKILL / 'scripts/check-prose.sh'), *args],
            input=text, text=True, capture_output=True,
            cwd=tempfile.gettempdir(), env=env,
        )

    def test_clean_and_findings(self):
        clean = self.run_check(text='I changed the file.\n')
        self.assertEqual(clean.returncode, 0, clean.stderr + clean.stdout)
        flagged = self.run_check(text='The docs say the flag is required.\n')
        self.assertEqual(flagged.returncode, 1, flagged.stderr + flagged.stdout)
        self.assertIn('The docs say the flag is required.', flagged.stdout)
        self.assertIn('\t', flagged.stdout)

    def test_document_with_spaces_is_not_modified(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'draft with spaces.md'
            path.write_text('I changed the file.\n', encoding='utf-8')
            before = path.read_bytes()
            result = self.run_check([str(path)])
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertEqual(path.read_bytes(), before)

    def test_source_comments(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'source.py'
            path.write_text('# The docs say the flag is required.\nx = 1\n', encoding='utf-8')
            before = path.read_bytes()
            result = self.run_check(['--path', str(path), str(path)])
            self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
            self.assertEqual(path.read_bytes(), before)

    def test_missing_input(self):
        with tempfile.TemporaryDirectory() as folder:
            result = self.run_check([str(Path(folder) / 'absent.md')])
        self.assertEqual(result.returncode, 2)
        self.assertIn('No such file', result.stderr)

    def test_missing_runtime(self):
        with tempfile.TemporaryDirectory() as folder:
            result = self.run_check(text='', env={**os.environ, 'XDG_DATA_HOME': folder})
        self.assertEqual(result.returncode, 2)
        self.assertIn('scripts/install.sh', result.stderr)

    def test_invalid_utf8_stdin(self):
        result = subprocess.run(
            ['bash', str(SKILL / 'scripts/check-prose.sh')],
            input=b'\xff\xfe\x00bad\n', capture_output=True,
        )
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn(b'utf-8', result.stderr)


if __name__ == '__main__':
    unittest.main()
