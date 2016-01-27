# coding: utf-8


class Service(object):
    """
    Base class for any buildable fixture.
    """

    def __init__(self, config=None):
        self.config = config

    def build(self):
        """
        Defines how to build concrete fixture. How to create usable artifacts.
        """

    def deploy(self):
        """
        Make artifacts available to use in tests.
        """

    def cleanup(self):
        """
        Removes all evidences.
        """
