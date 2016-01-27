# coding: utf-8
from .fixtures import make_fixtures
from .driver import WebDriver, web_driver
from .constants import DEFAULT_BROWSER, LOCAL_CAPABILITIES
from .helpers import generate_config, generate_name
from .screenshots import screenshoter


PARAMETRIZATION_CONFIG = {
    'web_driver': {
        'param_name': 'platforms',
        'default': [DEFAULT_BROWSER],
    },
    'screenshoter': {
        'param_name': 'screenshooter_platforms',
        'default': [None],
    }
}


def pytest_generate_tests(metafunc):
    """
    If there is `pytest.mark.platforms` mark on test, then use list of platforms passed to the mark.
    Else PLATFORMS will be used to parametrize `web_driver` and `screenshoter` fixtures.
    """
    for fixture_name, config in PARAMETRIZATION_CONFIG.items():
        if metafunc.config.getoption('--local'):
            platforms = [
                LOCAL_CAPABILITIES.get(browser) for browser in (metafunc.config.getoption('--browser') or ['firefox'])
            ]
        elif hasattr(metafunc.function, config['param_name']):
            platforms = getattr(metafunc.function, config['param_name']).args
        elif hasattr(metafunc.config, config['param_name']):
            platforms = getattr(metafunc.config, config['param_name'])
        else:
            platforms = config['default']
        if fixture_name in metafunc.fixturenames:
            ids = [generate_name(config) for config in platforms]
            metafunc.parametrize(fixture_name, platforms, ids=ids, indirect=True)


def pytest_addoption(parser):
    parser.addoption('--local', action='store_true', help='Enables local testing with WebDriver')
    parser.addoption('--browser', action='append', help='Browser class', choices=[
        'firefox', 'chrome', 'ie', 'edge', 'opera', 'safari'
    ])
