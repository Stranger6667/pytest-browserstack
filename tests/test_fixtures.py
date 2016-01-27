# coding: utf-8


# TODO. Fix coverage for tests


def test_make_fixtures(testdir):
    testdir.makepyfile('''
        from pytest_browserstack import make_fixtures
        from pytest_browserstack.services import Service


        make_fixtures(Service({'test': 'test'}))


        def test_make_fixtures(service):
            assert service.config == {'test': 'test'}
    ''')
    result = testdir.runpytest('--verbose')
    assert 'test_make_fixtures.py::test_make_fixtures PASSED' in result.stdout.lines


def test_fixture_scope(testdir):
    testdir.makepyfile('''
        from pytest_browserstack import make_fixtures
        from pytest_browserstack.services import Service


        class Container(Service):
            calls = []

            def __getattribute__(self, item):
                if item not in ('calls', '__class__'):
                    self.calls.append(item)
                return super(Container, self).__getattribute__(item)


        make_fixtures(Container())


        def test_first(container):
            assert container.calls == ['build', 'deploy']


        def test_second(container):
            assert container.calls == ['build', 'deploy']
    ''')
    result = testdir.runpytest('--verbose')
    assert 'test_fixture_scope.py::test_first PASSED' in result.stdout.lines
    assert 'test_fixture_scope.py::test_second PASSED' in result.stdout.lines


def test_make_fixtures_via_conftest(testdir):
    testdir.makeconftest('''
    from pytest_browserstack import make_fixtures
    from pytest_browserstack.services import Service


    class Dummy(Service):

        def test(self):
            return 'test'


    make_fixtures(Dummy())
    ''')
    testdir.makepyfile('''
    def test_make_fixtures(dummy):
        assert dummy.test() == 'test'
    ''')
    result = testdir.runpytest('--verbose')
    assert 'test_make_fixtures_via_conftest.py::test_make_fixtures PASSED' in result.stdout.lines


def test_methods_are_called(testdir):
    """
    Methods `build`, `deploy`, 'cleanup` should be called for every fixture.
    """
    # TODO. Test `cleanup`
    testdir.makepyfile('''
        from pytest_browserstack import make_fixtures
        from pytest_browserstack.services import Service


        class Container(Service):
            calls = []

            def __getattribute__(self, item):
                if item not in ('calls', '__class__'):
                    self.calls.append(item)
                return super(Container, self).__getattribute__(item)


        make_fixtures(Container())


        def test_methods_are_called(container):
            assert container.calls == ['build', 'deploy']
    ''')
    result = testdir.runpytest('--verbose')
    assert 'test_methods_are_called.py::test_methods_are_called PASSED' in result.stdout.lines
