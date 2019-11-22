from unittest import TestCase

from object_proxy import Proxy


class Foo(object):
    foo = 3


class TestProxy(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestProxy, self).__init__(*args, **kwargs)

        self.foo = None
        self.proxy = None

    def setUp(self):
        self.foo = Foo()
        self.proxy = Proxy(self.foo)

    def test_get_attribute(self):
        assert self.foo.foo == self.proxy.foo, "Proxy did not get the attribute of the original object"

    def test_set_attribute(self):
        expected = 6
        self.proxy.foo = expected
        assert self.foo.foo == expected, "Proxy did not set the attribute of the original object"
