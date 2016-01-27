# coding: utf-8


PATCHED_WEB_DRIVER = '''
try:
    from mock import patch
except ImportError:
    from unittest.mock import patch

from pytest_browserstack.driver import WebDriver


def pytest_configure(config):
    init = patch.object(WebDriver, '__init__', return_value=None)
    init.start()
    quit = patch.object(WebDriver, 'quit', return_value=None)
    quit.start()
    execute = patch.object(WebDriver, 'execute', return_value=None)
    execute.start()
    get_screenshot_as_base64 = patch.object(WebDriver, 'get_screenshot_as_base64', return_value='')
    get_screenshot_as_base64.start()
'''


def test_screenshot_save(testdir):
    testdir.makeconftest(PATCHED_WEB_DRIVER)
    testdir.makepyfile('''
    import os

    def test_name(web_driver):
        assert web_driver.save_screenshot('test')
        expected_path = os.path.join(os.getcwd(), 'test_screenshot_save', 'test_name')
        assert 'test-OS X El Capitan via Chrome 47.0 (1920x1080).png' in os.listdir(expected_path)
    ''')
    result = testdir.runpytest('--verbose')
    assert 'test_screenshot_save.py::test_name[OS X El Capitan via Chrome 47.0 (1920x1080)] PASSED' in result.stdout.lines


def test_class_based_test(testdir):
    testdir.makeconftest(PATCHED_WEB_DRIVER)
    testdir.makepyfile('''
    import os

    class TestScreenshot:

        def test_name(self, web_driver):
            assert web_driver.save_screenshot('test')
            expected_path = os.path.join(os.getcwd(), 'test_class_based_test', 'TestScreenshot', 'test_name')
            assert 'test-OS X El Capitan via Chrome 47.0 (1920x1080).png' in os.listdir(expected_path)
    ''')
    result = testdir.runpytest('--verbose')
    assert 'test_class_based_test.py::TestScreenshot::test_name[OS X El Capitan via Chrome 47.0 (1920x1080)] PASSED' in result.stdout.lines


def test_manual_screenshotdir_path(testdir):
    testdir.makeconftest(PATCHED_WEB_DRIVER + '''
    import os
    config.screenshots_dir = os.path.join(os.getcwd(), '..')
    ''')
    testdir.makepyfile('''
    import os

    def test_name(web_driver):
        assert web_driver.save_screenshot('test')
        expected_path = os.path.join(os.getcwd(), '..', 'test_manual_screenshotdir_path', 'test_name')
        assert 'test-OS X El Capitan via Chrome 47.0 (1920x1080).png' in os.listdir(expected_path)
    ''')
    result = testdir.runpytest('--verbose')
    assert 'test_manual_screenshotdir_path.py::test_name[OS X El Capitan via Chrome 47.0 (1920x1080)] PASSED' in result.stdout.lines
