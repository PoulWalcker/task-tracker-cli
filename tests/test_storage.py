import pytest
from app.exceptions import FileError
from app.storage import JSONStorage


def test_init_storage_fail():
    with pytest.raises(FileError) as e:
        JSONStorage(filename='storage.csv')
    assert e.value.args[0] == 'Storage must be in .json format only.'


def test_init_storage_no_creation(tmp_path):
    test_file = tmp_path / "test_storage.json"

    storage = JSONStorage(filename=str(test_file))

    assert storage.filepath.name.endswith('.json')
    assert storage.filepath.exists()
