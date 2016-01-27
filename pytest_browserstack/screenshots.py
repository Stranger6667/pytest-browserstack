# coding: utf-8
import pytest
from browserstacker import ScreenShotsAPI

from .constants import BROWSERSTACK_USER, BROWSERSTACK_KEY


@pytest.yield_fixture()
def screenshoter(request):
    """
    Instance of ScreenShotsAPI, parametrized with desired capabilities.
    """
    if hasattr(request, 'param'):
        browser = request.param
    else:
        browser = None
    api = ScreenShotsAPI(BROWSERSTACK_USER, BROWSERSTACK_KEY, default_browser=browser)
    yield api
    api.session.close()
