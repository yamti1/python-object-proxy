import fudge
from fudge import Fake
from unittest import TestCase, skip

from object_proxy import Proxy


class Foo(object):
    """
    Defines the target objects of the Proxy.
    """

    def __init__(self):
        self.value = 3


class TestProxy(TestCase):
    def setUp(self):
        """
        Creates a new orignial object and a new Proxy to it.
        """
        self.foo = Foo()
        self.proxy = Proxy(self.foo)

    def test_get_attribute(self):
        """
        Tests getting an attribute of the original object through the Proxy.
        """
        self.foo.value = 6
        self.assertEqual(self.foo.value, self.proxy.value, "Proxy did not get the attribute of the original object")

    def test_set_attribute(self):
        """
        Tests setting an attribute of the original object through the Proxy.
        """
        expected = 6
        self.foo.value = expected + 1
        self.proxy.value = expected
        self.assertEqual(self.foo.value, expected, "Proxy did not set the attribute of the original object")

    def test_del_attribute(self):
        """
        Tests deleting an attribute of the original object through the Proxy.
        """
        del self.proxy.value

        self.assertFalse(hasattr(self.foo, "value"),
                         "Attribute was not deleted on original object after deleting it on proxy")

    @fudge.test
    def test_method_call(self):
        """
        Tests calling a method of the original object through the Proxy.
        """
        expected = 6
        args = 1, 4, 5
        kwargs = {"a": 2, "b": 3}
        self.foo.func = Fake("func").expects_call().returns(expected).with_args(*args, **kwargs)

        result = self.proxy.func(*args, **kwargs)

        self.assertEqual(result, expected, "Call to a function through Proxy returned an unexpected result")

    def test_special_method_call(self):
        """
        Tests activating a special method of the original object through the Proxy.
        """
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
        """
        Tests the the Proxy's class has the same name, docstring and module name as the original object's class.
        """
        self.assertEqual(self.foo.__doc__, self.proxy.__doc__,
                         "Proxy's docstring does not match original object's docstring")

        self.assertEqual(self.foo.__module__, self.proxy.__module__,
                         "Proxy's module does not match original object's module")

        self.assertEqual(self.foo.__class__.__name__, self.proxy.__class__.__name__,
                         "Proxy's class name does not match original object's class name")

    @skip("TODO")
    def test_weakref(self):
        pass

    def test_child_class(self):
        """
        Tests that the Proxy can properly all a special method defined in a base class of the original object.
        """

        expected = range(10)

        class Base(object):
            def __iter__(self):
                return iter(expected)

        class Child(Base):
            pass

        child = Child()
        proxy = Proxy(child)

        result = [num for num in proxy]
        self.assertEqual(result, expected)

    def test_custom_getattr(self):
        """
        Tests that the Proxy calls the original object's `__getattr__` properly.
        """
        class Boo(object):
            expected_key = "val"
            expected_value = 9

            def __init__(self):
                self.got_expected_key = False

            def __getattr__(self, key):
                self.got_expected_key = key == Boo.expected_key
                return Boo.expected_value

        boo = Boo()
        proxy = Proxy(boo)
        result = getattr(proxy, Boo.expected_key)

        self.assertEqual(Boo.expected_value, result,
                         "Proxy did not return the expected result from __getattr__ of the original object.")
        self.assertTrue(boo.got_expected_key,
                        "Proxy did not call custom __getattr__ of the original object with the correct key.")

    def test_custom_setattr(self):
        """
        Tests that the Proxy calls the original object's `__setattr__` properly.
        """
        class Boo(object):
            expected_key = "val"
            expected_value = 9

            def __init__(self):
                self.got_expected_key = False
                self.got_expected_value = False

            def __setattr__(self, key, value):
                object.__setattr__(self, "got_expected_key", key == Boo.expected_key)
                object.__setattr__(self, "got_expected_value", value == Boo.expected_value)

        boo = Boo()
        proxy = Proxy(boo)
        setattr(proxy, Boo.expected_key, Boo.expected_value)

        self.assertTrue(boo.got_expected_key,
                        "Proxy did not call custom __setattr__ of the original object with the correct key.")
        self.assertTrue(boo.got_expected_value,
                        "Proxy did not call custom __setattr__ of the original object with the correct value.")

    def test_custom_deltattr(self):
        """
        Tests that the Proxy calls the original object's `__delattr__` properly.
        """
        class Boo(object):
            expected_key = "val"

            def __init__(self):
                self.got_expected_key = False

            def __delattr__(self, key):
                self.got_expected_key = key == Boo.expected_key

        boo = Boo()
        proxy = Proxy(boo)
        delattr(proxy, Boo.expected_key)

        self.assertTrue(boo.got_expected_key,
                        "Proxy did not call custom __delattr__ of the original object with the correct key.")

    @skip("TODO")
    def test_custom_getattribute(self):
        pass