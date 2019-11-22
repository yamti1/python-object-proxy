import fudge
from fudge import Fake
from unittest import TestCase

from object_proxy import Proxy


class Foo(object):
    """
    Defines the target objects of the Proxy.
    """

    def __init__(self):
        self.value = 3


class TestProxy(TestCase):
    def setUp(self):
        self.foo = Foo()
        self.proxy = Proxy(self.foo)

    def test_get_attribute(self):
        self.foo.value = 6
        self.assertEqual(self.foo.value, self.proxy.value, "Proxy did not get the attribute of the original object")

    def test_set_attribute(self):
        expected = 6
        self.proxy.value = expected
        self.assertEqual(self.foo.value, expected, "Proxy did not set the attribute of the original object")

    def test_del_attribute(self):
        del self.foo.value

        self.assertFalse(hasattr(self.proxy, "value"),
                         "Attribute in Proxy was not deleted after deleting it in the original object")

    @fudge.test
    def test_method_call(self):
        expected = 6
        args = 1, 4, 5
        kwargs = {"a": 2, "b": 3}
        self.foo.func = Fake("func").expects_call().returns(expected).with_args(*args, **kwargs)

        result = self.proxy.func(*args, **kwargs)

        self.assertEqual(result, expected, "Call to a function through Proxy returned an unexpected result")

    def test_special_method_call(self):
        expected = range(10)

        # Special Methods require the object's class to define them so
        # setting `self.foo.__iter__` to a `fudge.Fake` won't work.
        class Foo(object):
            def __iter__(self):
                return iter(expected)

        self.foo = Foo()
        self.proxy = Proxy(self.foo)

        result = [num for num in self.proxy]
        self.assertEqual(result, expected,
                         "A call to a special method `__iter__` on the Proxy returned an unexpected result")

    def test_class_metadata(self):
        self.assertEqual(self.foo.__doc__, self.proxy.__doc__,
                         "Proxy's docstring does not match original object's docstring")

        self.assertEqual(self.foo.__module__, self.proxy.__module__,
                         "Proxy's module does not match original object's module")
