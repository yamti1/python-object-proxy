import fudge
from fudge import Fake
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

    @fudge.test
    def test_method_call(self):
        expected = 6
        args = 1, 4, 5
        kwargs = {"a": 2, "b": 3}
        self.foo.func = Fake("func").expects_call().returns(expected).with_matching_args(*args, **kwargs)

        result = self.proxy.func(*args, **kwargs)

        assert result == expected, "Call to a function through Proxy returned an unexpected result"
