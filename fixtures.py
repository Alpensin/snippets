import alembic
import pytest
from alembic.config import Config
from flask_tools.config_loader import get_config

from api.app import flask_app

from .db_data.clickhouse_storage_db.base_data import insert_storage_db_data

TEST_DB_ALEMBIC_CONFIGS = (Config("database/config/alembic.ini"), Config("database/clickhouse/alembic.ini"))


@pytest.fixture(scope="session", autouse=True)
def check_is_testing_env() -> None:
    settings = get_config('api.config')
    if not settings.ENV_PREFIX.startswith('TESTING_'):
        raise RuntimeError('Check that it is test environment and ENV_PREFIX starts with TESTING_')


@pytest.fixture
def client():
    app = flask_app.create_app()

    if not app.config['ENV_PREFIX'].startswith('TESTING_'):
        raise RuntimeError('Check that it is test environment and ENV_PREFIX starts with TESTING_')

    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture(scope="session", autouse=True)
def apply_migrations(check_is_testing_env):
    for config in TEST_DB_ALEMBIC_CONFIGS:
        alembic.command.upgrade(config, "head")
    yield
    for config in TEST_DB_ALEMBIC_CONFIGS:
        alembic.command.downgrade(config, "base")


@pytest.fixture(scope="session", autouse=True)
def insert_base_data(apply_migrations) -> None:
    insert_storage_db_data()


@pytest.fixture(scope="function")
def restore_db_after_use(check_is_testing_env):
    yield
    for config in TEST_DB_ALEMBIC_CONFIGS:
        alembic.command.downgrade(config, "base")
    for config in TEST_DB_ALEMBIC_CONFIGS:
        alembic.command.upgrade(config, "head")
    insert_storage_db_data()
