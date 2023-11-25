from pathlib import Path

## https://docs.pytest.org/
import pytest

def pytest_addoption(parser):
    """Add additional argument/options/flags to the command-line

    See Also:
      * https://docs.pytest.org/en/latest/reference.html#pytest.hookspec.pytest_addoption
    """
    parser.addoption('--address', default='127.0.0.1:8888', help='ip address and port to use')

@pytest.fixture(scope='session')
def address(request) -> str:
    """Return the address as provided by --address"""
    return request.config.getoption('--address')
