import csv
import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / 'data'

NULL = 'NULL'
OMITTED = 'OMITTED'


def rows(filename):
    with open(DATA_DIR / filename, newline='') as handle:
        return list(csv.DictReader(handle))


def get_value(value):
    if value == NULL:
        return None
    return value


def get_omitted_keys(row):
    return [key for key, value in row.items() if value == OMITTED]


def by_key(elements, key):
    return {element[key]: element for element in elements}


def elements_of(cell, key):
    return by_key(json.loads(cell), key)
