import json
from contextlib import contextmanager


@contextmanager
def open_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    before = json.dumps(data, sort_keys=True)

    yield data

    after = json.dumps(data, sort_keys=True)

    if after != before:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
