from django.test import TestCase
from commons.dependency import provider, requires, get_provider


class DependencyTest(TestCase):
    @provider('p1')
    class Provider1:
        def __init__(self):
            print 'Provider1'

    @provider('p2')
    class Provider2:
        def __init__(self):
            print 'Provider2'

    @requires('p1', 'p2')
    class Consumer:
        def __init__(self):
            p1 = get_provider('p1')
            p2 = get_provider('p2')

    def test(self):
        c = DependencyTest.Consumer()
