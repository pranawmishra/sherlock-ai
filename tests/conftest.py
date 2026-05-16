import pytest
from sherlock_ai import SherlockAI, LoggingConfig

@pytest.fixture(scope="session")
def sherlock_instance(tmp_path_factory):
    logs_dir = tmp_path_factory.mktemp("logs")
    config = LoggingConfig(logs_dir=str(logs_dir), auto_instrument=False)
    instance = SherlockAI(config=config)
    instance.setup()
    yield instance
    instance.cleanup()

@pytest.fixture
def default_config():
    return LoggingConfig()