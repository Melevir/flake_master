import pytest


@pytest.fixture
def preset_file_path():
    return 'test.yml'


@pytest.fixture
def preset_url():
    return 'https://example.com/test.yml'


@pytest.fixture
def preset_file_content():
    return '''[info]
name = test_preset
revision = 6

[flake8_plugins]
pydocstyle = 3.0.0

[flake8_config]
max-complexity = 18'''
