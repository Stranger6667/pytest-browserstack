# coding: utf-8
import os


DEFAULT_RESOLUTION = '1920x1080'
BROWSERSTACK_USER = os.environ.get('BROWSERSTACK_USER')
BROWSERSTACK_KEY = os.environ.get('BROWSERSTACK_KEY')
COMMAND_EXECUTOR = 'http://%s:%s@hub.browserstack.com:80/wd/hub' % (BROWSERSTACK_USER, BROWSERSTACK_KEY)
DEFAULT_BROWSER = {
    'browser': 'Chrome',
    'browser_version': '47.0',
    'os': 'OS X',
    'os_version': 'El Capitan',
    'resolution': DEFAULT_RESOLUTION
}

LOCAL_CAPABILITIES = {
    'firefox': {
        'browser_name': 'Firefox',
        'resolution': DEFAULT_RESOLUTION,
    },
    'chrome': {
        'browser_name': 'Chrome',
        'resolution': DEFAULT_RESOLUTION,
    },
    'ie': {
        'browser_name': 'Internet Explorer',
        'resolution': DEFAULT_RESOLUTION,
    },
    'edge': {
        'browser_name': 'Edge',
        'resolution': DEFAULT_RESOLUTION,
    },
    'opera': {
        'browser_name': 'Opera',
        'resolution': DEFAULT_RESOLUTION,
    },
    'safari': {
        'browser_name': 'Safari',
        'resolution': DEFAULT_RESOLUTION,
    }
}
