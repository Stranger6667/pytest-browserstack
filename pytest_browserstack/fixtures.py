# coding: utf-8
import inspect
import sys


FIXTURE_TEMPLATE = '''
import pytest


@pytest.yield_fixture(scope='session')
def {name}():
    instance.build()
    instance.deploy()
    yield instance
    instance.cleanup()
'''


def make_fixtures(*instances):
    """
    Creates fixtures for given build instances.
    """
    for instance in instances:
        func_name = instance.__class__.__name__.lower()
        context = {'instance': instance}
        exec(FIXTURE_TEMPLATE.format(name=func_name), context)
        fixture_func = context[func_name]
        module = get_caller_module()
        fixture_func.__module__ = module
        setattr(module, func_name, fixture_func)


def get_caller_module(depth=2):
    """
    Get the module of the caller.
    """
    frame = sys._getframe(depth)
    module = inspect.getmodule(frame)
    # Happens when there's no __init__.py in the folder
    if module is None:
        return get_caller_module(depth=depth)
    return module
