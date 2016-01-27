# coding: utf-8


def test_screenshoter_available(testdir):
    """
    `screenshoter` fixture should be available for test run.
    """
    result = testdir.runpytest('--fixtures')
    assert '    Instance of ScreenShotsAPI, parametrized with desired capabilities.' in result.stdout.lines
