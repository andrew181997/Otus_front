import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--log-file",
        action="store",
        default=None,
        help="Path to single log file"
    )
    parser.addoption(
        "--log-dir",
        action="store",
        default=None,
        help="Path to directory with logs"
    )
    parser.addoption(
        "--output",
        action="store",
        default="output.json",
        help="Output file path"
    )

@pytest.fixture
def log_path(request):
    return {
        "file": request.config.getoption("--log-file"),
        "dir": request.config.getoption("--log-dir"),
        "output": request.config.getoption("--output")
    }