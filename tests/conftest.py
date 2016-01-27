# coding: utf-8
import pytest

from ._compat import patch, Mock


pytest_plugins = 'pytester'


@pytest.fixture
def mocked_request(request):
    mock = patch('requests.request', Mock())
    mock.start()
    request.addfinalizer(mock.stop)
    return mock.new
