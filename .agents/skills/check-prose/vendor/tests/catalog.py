from pathlib import Path


PROJECT = Path(__file__).resolve().parent.parent

INTERPRETER = PROJECT / 'venv' / 'bin' / 'python'
CHECKER = PROJECT / 'check_prose.py'
PHRASES = PROJECT / 'phrases.txt'


def seed_catalog():
    """Prove that three files are there before the first row runs.

    A command has no store to seed. I run the command itself for every
    row. The three files are the interpreter, the command, and the phrase
    list.

    The caller passes strict as True here. Python then raises OSError
    when no file exists at that path. Nobody runs a row when a file is
    missing. It does not fail every row on its own.

    See https://docs.python.org/3/library/pathlib.html for Path.resolve.
    """
    INTERPRETER.resolve(strict=True)
    CHECKER.resolve(strict=True)
    PHRASES.resolve(strict=True)
