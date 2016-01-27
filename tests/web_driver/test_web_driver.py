# coding: utf-8
import pytest


PATCHED_WEB_DRIVER = '''
try:
    from mock import patch
except ImportError:
    from unittest.mock import patch


def pytest_configure(config):
    patcher = patch('pytest_browserstack.driver.WebDriver')
    patcher.start()
    patcher = patch('pytest_browserstack.driver.get_webdriver_class')
    patcher.start()
'''


def test_web_driver_available(testdir):
    """
    `web_driver` fixture should be available for test run.
    """
    result = testdir.runpytest('--fixtures')
    assert '    Defines WebDriver instance with desired capabilities.' in result.stdout.lines


def test_web_driver_instance(testdir):
    testdir.makeconftest(PATCHED_WEB_DRIVER)
    testdir.makepyfile('''
    def test_web_driver_instance(web_driver):
        web_driver._mock_new_parent.assert_called_with(
            command_executor='http://None:None@hub.browserstack.com:80/wd/hub',
            desired_capabilities={
                'os_version': 'El Capitan',
                'browser': 'Chrome',
                'os': 'OS X',
                'browser_version': '47.0',
                'resolution': '1920x1080'
            })
    ''')
    result = testdir.runpytest('--verbose')
    assert 'test_web_driver_instance.py::test_web_driver_instance[OS X El Capitan via Chrome 47.0 (1920x1080)] PASSED' in result.stdout.lines


@pytest.mark.parametrize(
    'run_args, kwargs',
    (
        (
            ('--verbose', ),
            {
                'command_executor': 'http://None:None@hub.browserstack.com:80/wd/hub',
                'desired_capabilities': {
                    'resolution': '1920x1080',
                    'browser_version': '47.0',
                    'browser': 'Chrome',
                    'os': 'OS X',
                    'unexpectedAlertBehaviour': 'ignore',
                    'os_version': 'El Capitan'
                }
            }
        ),
        (
            ('--verbose', '--local'),
            {
                'capabilities': {
                    'platform': 'ANY',
                    'javascriptEnabled': True,
                    'marionette': False,
                    'unexpectedAlertBehaviour': 'ignore',
                    'version': '',
                    'browserName': 'firefox'
                }
            }
        ),
    )
)
def test_custom_capabilities(testdir, run_args, kwargs):
    testdir.makeconftest(PATCHED_WEB_DRIVER)
    testdir.makepyfile('''
    import pytest

    @pytest.mark.capabilities({'unexpectedAlertBehaviour': 'ignore'})
    def test_web_driver_instance(web_driver):
        web_driver._mock_new_parent.assert_called_with(**%s)
    ''' % str(kwargs))
    result = testdir.runpytest(*run_args)
    assert 'PASSED' in ''.join(result.stdout.lines)


def test_platforms_mark(testdir):
    testdir.makeconftest(PATCHED_WEB_DRIVER)
    testdir.makepyfile('''
    import pytest


    PLATFORMS = [
        {'browser': 'IE', 'browser_version': '8.0', 'os': 'Windows', 'os_version': '7', 'resolution': '1024x768'},
        {'browserName': 'iPhone', 'platform': 'MAC', 'device': 'iPhone 6S Plus'},
    ]


    @pytest.mark.platforms(*PLATFORMS)
    def test_platforms_mark(web_driver):
        pass
    ''')
    result = testdir.runpytest('--collect-only')
    assert "  <Function 'test_platforms_mark[Windows 7 via IE 8.0 (1024x768)]'>" in result.stdout.lines
    assert "  <Function 'test_platforms_mark[iPhone 6S Plus (MAC) via iPhone]'>" in result.stdout.lines


def test_register_platforms(testdir):
    testdir.makeconftest('''
    PLATFORMS = [
        {'browser': 'IE', 'browser_version': '8.0', 'os': 'Windows', 'os_version': '7', 'resolution': '1920x1080'},
        {'browserName': 'iPhone', 'platform': 'MAC', 'device': 'iPhone 6'},
    ]

    def pytest_configure(config):
        config.platforms = PLATFORMS
    ''')
    testdir.makepyfile('''
    def test_platforms_mark(web_driver):
        pass
    ''')
    result = testdir.runpytest('--collect-only')
    assert "  <Function 'test_platforms_mark[Windows 7 via IE 8.0 (1920x1080)]'>" in result.stdout.lines
    assert "  <Function 'test_platforms_mark[iPhone 6 (MAC) via iPhone]'>" in result.stdout.lines


def test_mixed_platforms(testdir):
    testdir.makeconftest('''
    PLATFORMS = [
        {'browserName': 'iPhone', 'platform': 'MAC', 'device': 'iPhone 6'},
    ]

    def pytest_configure(config):
        config.platforms = PLATFORMS
    ''')
    testdir.makepyfile(
        test_global='''
        def test_global(web_driver):
            pass
        ''',
        test_local='''
        import pytest


        PLATFORMS = [
            {'browser': 'IE', 'browser_version': '8.0', 'os': 'Windows', 'os_version': '7', 'resolution': '1920x1080'}
        ]

        @pytest.mark.platforms(*PLATFORMS)
        def test_local(web_driver):
            pass
        '''
    )
    result = testdir.runpytest('--collect-only')
    assert "  <Function 'test_local[Windows 7 via IE 8.0 (1920x1080)]'>" in result.stdout.lines
    assert "  <Function 'test_global[iPhone 6 (MAC) via iPhone]'>" in result.stdout.lines


def test_local_option(testdir):
    testdir.makeconftest(PATCHED_WEB_DRIVER)
    testdir.makepyfile('''
    def test_platforms_mark(web_driver):
        pass
    ''')
    result = testdir.runpytest('--collect-only', '--local', '--browser', 'ie', '--browser', 'firefox', '-s')
    output = ''.join(result.stdout.lines)
    assert output.count("<Function 'test_platforms_mark") == 2
    assert "via Internet Explorer Unknown (1920x1080)]'>" in output
    assert "via Firefox Unknown (1920x1080)]'>" in output
