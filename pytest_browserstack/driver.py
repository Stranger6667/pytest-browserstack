# coding: utf-8
import os
import re

import pytest
from py.path import local
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from .constants import COMMAND_EXECUTOR


screenshot_path_regex = re.compile(
    '(?P<module_name>.*?).py::'
    '(?P<class_name>[\w]*?)[:\(\)]*?'
    '(?P<func_name>[\w]*?)\['
    '(?P<browser_info>.*?)\]'
)


class BaseWebDriver(object):
    request = None
    w3c = None

    def save_screenshot(self, filename):
        filename = self.generate_filename(filename)
        return super(BaseWebDriver, self).save_screenshot(filename)

    def generate_filename(self, filename):
        nodeid = self.request._pyfuncitem._nodeid
        groups = screenshot_path_regex.search(nodeid).groups()
        basedir = local(os.path.join(self.screenshots_dir, *groups[:-1]))
        basedir.ensure(dir=True)
        return str(basedir / filename + '-' + groups[-1] + '.png')

    @property
    def screenshots_dir(self):
        if hasattr(self.request.config, 'screenshots_dir'):
            return str(self.request.config.screenshots_dir)
        return str(self.request._fixturemanager.config.rootdir)

    def __repr__(self):
        return self.__class__.__name__


class WebDriver(BaseWebDriver, webdriver.Remote):
    pass


def get_webdriver_class(base_class):

    class LocalWebDriver(BaseWebDriver, base_class):
        pass

    return LocalWebDriver


@pytest.yield_fixture()
def web_driver(request):
    """
    Defines WebDriver instance with desired capabilities.
    You can pass capabilities via `pytest.mark.platforms` on test
    or via `pytest_configure` to parametrize tests globally.
    """
    config = request.param
    marker = request.node.get_marker('capabilities')
    if marker:
        extra_capabilities = marker.args[0]
    else:
        extra_capabilities = None

    if request.config.getoption('--local'):
        base_class = {
            'Firefox': webdriver.Firefox,
            'Chrome': webdriver.Chrome,
            'Internet Explorer': webdriver.Ie,
            'Edge': webdriver.Edge,
            'Opera': webdriver.Opera,
            'Safari': webdriver.Safari,
        }.get(config['browser_name'], webdriver.Firefox)

        web_driver_class = get_webdriver_class(base_class)

        capabilities = {
            'Firefox': DesiredCapabilities.FIREFOX,
            'Chrome': DesiredCapabilities.CHROME,
            'Internet Explorer': DesiredCapabilities.INTERNETEXPLORER,
            'Edge': DesiredCapabilities.EDGE,
            'Opera': DesiredCapabilities.OPERA,
            'Safari': DesiredCapabilities.SAFARI,
        }.get(config['browser_name'], DesiredCapabilities.FIREFOX)
        if extra_capabilities:
            capabilities.update(extra_capabilities)

        key = {
            'Firefox': 'capabilities',
            'Chrome': 'desired_capabilities',
            'Internet Explorer': 'capabilities',
            'Edge': 'capabilities',
            'Opera': 'desired_capabilities',
            'Safari': 'desired_capabilities',
        }.get(config['browser_name'])
        driver = web_driver_class(**{key: capabilities})
    else:
        if extra_capabilities:
            config.update(extra_capabilities)
        driver = WebDriver(command_executor=COMMAND_EXECUTOR, desired_capabilities=config)
    driver.request = request
    driver.is_mobile = bool(config.get('platform', False))
    if 'resolution' in config:
        w, h = config['resolution'].split('x')
        driver.set_window_size(w, h)
    try:
        driver.implicitly_wait(30)
        driver.set_page_load_timeout(30)
    except:
        pass
    yield driver
    driver.quit()
