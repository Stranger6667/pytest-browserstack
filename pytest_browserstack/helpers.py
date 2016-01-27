# coding: utf-8
import platform


def generate_name(browser):
    browser = browser.copy()
    browser.setdefault('browser_version', 'Unknown')
    browser.setdefault('resolution', 'Unknown')
    browser.setdefault('browserName', browser.get('browser'))
    browser.setdefault('browser', browser.get('browser_name'))
    if browser.get('device'):
        browser.setdefault('platform', browser.get('os'))
        return '%(device)s (%(platform)s) via %(browserName)s' % browser
    else:
        if 'os' not in browser:
            browser['os'] = platform.system()
            browser['os_version'] = platform.release()
        return '%(os)s %(os_version)s via %(browser)s %(browser_version)s (%(resolution)s)' % browser


def generate_config(platforms, browsers_settings):
    """
    Generation config for parametrize tests by platforms, browsers and screen resolutions.

    :param platforms: Dict with platforms settings.
    :param browsers_settings: Browsers for each platform.
    :returns: Generator for list of dictionaries.
    """
    configs = []
    for base, params in browsers_settings.items():
        browsers, resolutions = params
        for browser in browsers:
            new_config = platforms[base].copy()
            new_config.update(browser)
            if resolutions:
                for resolution in resolutions:
                    new_config = new_config.copy()
                    new_config['resolution'] = '%sx%s' % resolution
                    configs.append(new_config)
            else:
                configs.append(new_config)
    return configs
