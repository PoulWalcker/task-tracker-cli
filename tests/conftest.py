import pytest
from app.storage import JSONStorage


@pytest.fixture
def storage(tmp_path):
    db_filename = tmp_path / "test_storage.json"
    return JSONStorage(str(db_filename))
