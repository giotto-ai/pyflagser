import pytest


def pytest_addoption(parser):
    parser.addoption("--webdl",
                     action="store_true",
                     default=False,
                     help="Whether or not to download files "
                          "required for testing from the web")


@pytest.fixture
def webdl(request):
    return request.config.getoption("--webdl")
