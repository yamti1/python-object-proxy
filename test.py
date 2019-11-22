from unittest import TestCase

from object_proxy import Proxy


class Foo(object):
    def __init__(self):
        self.value = 3


class TestProxy(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestProxy, self).__init__(*args, **kwargs)

        self.foo = None
        self.proxy = None

    def setUp(self):
        self.foo = Foo()
        self.proxy = Proxy(self.foo)

    def test_get_attribute(self):
        self.foo.value = 6
        assert self.foo.value == self.proxy.value, "Proxy did not get the attribute of the original object"

    def test_set_attribute(self):
        expected = 6
        self.proxy.value = expected
        assert self.foo.value == expected, "Proxy did not set the attribute of the original object"

    def test_del_attribute(self):
        del self.foo.value

        msg = "Attribute in Proxy was not deleted after deleting it in the original object"
        assert not hasattr(self.proxy, "value"), msg
