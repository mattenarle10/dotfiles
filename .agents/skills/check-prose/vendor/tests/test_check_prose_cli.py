import json
import subprocess
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from catalog import CHECKER, INTERPRETER, seed_catalog
from test_helpers import get_value, rows


CANNOT_READ = 2

# The command needs 0.83 seconds for one text, and the model load takes
# almost all of that time. I keep this many calls open at once, and I get the whole
# suite back in three minutes.
WORKERS = 8

# The user sends text to the command in three ways. The checker pulls the
# prose out of each one and then reads it the same way.
EVERY_FORM = ('stdin', 'document', 'source')

COMMENT_SIGN = '# '
DOCUMENT_NAME = 'doc.md'
SOURCE_NAME = 'mod.py'

EVERY_FORM_COLUMN = '|'.join(EVERY_FORM)


def as_comments(text):
    lines = [COMMENT_SIGN + line for line in text.splitlines()]
    return '\n'.join(lines) + '\n'


def as_is(text):
    return text


# I pick the file name, the wrapper around the text, and the words on
# the command line out of the form. Each one is a lookup rather than a branch.
FILE_NAME = {'document': DOCUMENT_NAME, 'source': SOURCE_NAME}
WRAPPER = {'document': as_is, 'source': as_comments}
ARGUMENTS = {
    'document': lambda path: [str(INTERPRETER), str(CHECKER), str(path)],
    'source': lambda path: [
        str(INTERPRETER), str(CHECKER), '--path', str(path), str(path),
    ],
}


class CheckProseCliTest(unittest.TestCase):

    _INTERFACE = 'command'

    @classmethod
    def setUpClass(cls):
        seed_catalog()

    def test_check_text(self):
        jobs = [
            (row, form)
            for name in ('check_success.csv', 'check_failure.csv')
            for row in rows(name)
            for form in (row['form'] or EVERY_FORM_COLUMN).split('|')
        ]
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            results = list(pool.map(self._run_one, jobs))
        for job, result in zip(jobs, results):
            row, form = job
            with self.subTest(description=row['description'], form=form):
                self._check_the_run(row, form, result)

    def _run_one(self, job):
        """Run the command once and hand back what it printed and wrote."""
        row, form = job
        runner = {'stdin': self._run_on_stdin}.get(form, self._run_on_a_file)
        return runner(row, form)

    def _run_on_stdin(self, row, form):
        finished = subprocess.run(
            [str(INTERPRETER), str(CHECKER)],
            input=get_value(row['text']), capture_output=True, text=True,
        )
        return finished, b'', b''

    def _run_on_a_file(self, row, form):
        """Write the text as this form holds it, then check that file.

        Some rows have their own file name. I already wrote the markers
        into the text of those rows. I wrap a shared row as a comment on
        every line of the source file.
        """
        text = get_value(row['text'])
        # I already wrote the markers into the text of those rows.
        wrapper = {'': WRAPPER[form]}.get(row['filename'], as_is)
        written = wrapper(text)
        name = row['filename'] or FILE_NAME[form]
        with tempfile.TemporaryDirectory() as workspace:
            path = Path(workspace) / name
            path.write_text(written, encoding='utf-8')
            finished = subprocess.run(
                ARGUMENTS[form](path), input='', capture_output=True,
                text=True,
            )
            # I compare the bytes. Python turns a carriage return into a
            # newline on a text read. A row with a carriage return would
            # then look like a file the command had rewritten.
            return finished, written.encode('utf-8'), path.read_bytes()

    def _check_the_run(self, row, form, result):
        finished, written, after = result
        printed = finished.stdout.splitlines()
        expected = json.loads(row['findings'])
        self.assertEqual(
            finished.returncode, int(row['exit_code']),
            f'{row["description"]} as {form}: the command exited {finished.returncode} and printed {printed}',
        )
        self.assertEqual(
            len(printed), int(row['findings_count']),
            f'{row["description"]} as {form}: it printed {len(printed)} findings',
        )
        self.assertEqual(
            finished.stderr, get_value(row['stderr']),
            f'{row["description"]} as {form}: it wrote {finished.stderr!r} to stderr',
        )
        for line in printed:
            self.assertIn(
                line, expected,
                f'{row["description"]} as {form}: it printed {line!r}, which no column states',
            )
        self.assertEqual(
            after, written,
            f'{row["description"]} as {form}: the file now holds different text',
        )

    def test_check_a_chat_message_answers_the_four_blind_calls(self):
        finished = subprocess.run(
            [str(INTERPRETER), str(CHECKER)],
            stdin=subprocess.DEVNULL, capture_output=True, text=True,
        )
        self.assertEqual(
            finished.returncode, 0,
            f'a message carrying nothing at all exited {finished.returncode}',
        )

        finished = subprocess.run(
            [str(INTERPRETER), str(CHECKER)],
            input='', capture_output=True, text=True,
        )
        self.assertEqual(
            finished.returncode, 0,
            f'a message of no characters exited {finished.returncode}',
        )

        finished = subprocess.run(
            [str(INTERPRETER), str(CHECKER)],
            input='\x00\n', capture_output=True, text=True,
        )
        self.assertEqual(
            finished.returncode, 0,
            f'a message holding a null character exited {finished.returncode}',
        )

        finished = subprocess.run(
            [str(INTERPRETER), str(CHECKER)],
            input=b'\xff\xfe\x00bad\n', capture_output=True,
        )
        self.assertEqual(
            finished.returncode, CANNOT_READ,
            f'a message the command cannot read exited {finished.returncode}',
        )

    def test_check_a_document_answers_the_four_blind_calls(self):
        finished = subprocess.run(
            [str(INTERPRETER), str(CHECKER)],
            stdin=subprocess.DEVNULL, capture_output=True, text=True,
        )
        self.assertEqual(
            finished.returncode, 0,
            f'a call naming no document at all exited {finished.returncode}',
        )

        finished = subprocess.run(
            [str(INTERPRETER), str(CHECKER), ''],
            input='', capture_output=True, text=True,
        )
        self.assertEqual(
            finished.returncode, CANNOT_READ,
            f'a document name of no characters exited {finished.returncode}',
        )

        with tempfile.TemporaryDirectory() as workspace:
            absent = Path(workspace) / 'absent.md'
            finished = subprocess.run(
                [str(INTERPRETER), str(CHECKER), str(absent)],
                input='', capture_output=True, text=True,
            )
            self.assertEqual(
                finished.returncode, CANNOT_READ,
                f'a document name that holds no file exited {finished.returncode}',
            )

            unreadable = Path(workspace) / 'unreadable.md'
            unreadable.write_bytes(b'\xff\xfe\x00bad\n')
            finished = subprocess.run(
                [str(INTERPRETER), str(CHECKER), str(unreadable)],
                input='', capture_output=True, text=True,
            )
            self.assertEqual(
                finished.returncode, CANNOT_READ,
                f'a document the command cannot read exited {finished.returncode}',
            )

    def test_check_a_source_file_answers_the_four_blind_calls(self):
        finished = subprocess.run(
            [str(INTERPRETER), str(CHECKER), '--path'],
            input='', capture_output=True, text=True,
        )
        self.assertEqual(
            finished.returncode, CANNOT_READ,
            f'a call naming nothing after --path exited {finished.returncode}',
        )

        with tempfile.TemporaryDirectory() as workspace:
            source = Path(workspace) / 'mod.py'
            source.write_text('x = 1\n', encoding='utf-8')
            finished = subprocess.run(
                [str(INTERPRETER), str(CHECKER), '--path', '', str(source)],
                input='', capture_output=True, text=True,
            )
            self.assertEqual(
                finished.returncode, 0,
                f'a name of no characters after --path exited {finished.returncode}',
            )

            finished = subprocess.run(
                [str(INTERPRETER), str(CHECKER), '--path', str(source)],
                stdin=subprocess.DEVNULL, capture_output=True, text=True,
            )
            self.assertEqual(
                finished.returncode, 0,
                f'a call naming no source file exited {finished.returncode}',
            )

            unreadable = Path(workspace) / 'unreadable.py'
            unreadable.write_bytes(b'\xff\xfe\x00bad\n')
            finished = subprocess.run(
                [str(INTERPRETER), str(CHECKER), '--path', str(unreadable), str(unreadable)],
                input='', capture_output=True, text=True,
            )
            self.assertEqual(
                finished.returncode, CANNOT_READ,
                f'a source file the command cannot read exited {finished.returncode}',
            )

    def test_the_command_refuses_every_other_argument_shape(self):
        finished = subprocess.run(
            [str(INTERPRETER), str(CHECKER), '--verbose'],
            input='', capture_output=True, text=True,
        )
        self.assertEqual(
            finished.returncode, CANNOT_READ,
            f'the command has no --verbose and exited {finished.returncode}',
        )

        finished = subprocess.run(
            [str(INTERPRETER), str(CHECKER), '--help'],
            input='', capture_output=True, text=True,
        )
        self.assertEqual(
            finished.returncode, CANNOT_READ,
            f'the command has no --help and exited {finished.returncode}',
        )

        finished = subprocess.run(
            [str(INTERPRETER), str(CHECKER), '-p', 'x.py'],
            input='', capture_output=True, text=True,
        )
        self.assertEqual(
            finished.returncode, CANNOT_READ,
            f'the command has no -p and exited {finished.returncode}',
        )
