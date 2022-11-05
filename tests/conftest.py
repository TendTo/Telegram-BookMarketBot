"""Test configuration"""
from typing import Iterable
import pytest
from module.shared import DB_PATH

config_map = {}


@pytest.fixture(scope="session", autouse=True)
def setup_config():
    """Called at the beginning of the testing session.
    Overrides the test configuration
    """
    # store a copy of the normal configuration
    old_configuration = {}
    for k, val in config_map.items():
        old_configuration[k] = val

    # override normal configuration with test configuration
    for k, val in config_map.get("test", {}).items():
        config_map[k] = val

    yield  # run the tests

    # restore the normal configuration
    for k, val in old_configuration.items():
        config_map[k] = val


@pytest.fixture(scope="session", autouse=True)
def setup_db_path() -> Iterable[str]:
    """Mocks the sqlite3.connect method and returns a mocked connection"""
    global DB_PATH
    temp = DB_PATH
    DB_PATH = "test.db"
    yield DB_PATH
    DB_PATH = temp
