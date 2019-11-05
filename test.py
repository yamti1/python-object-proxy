from object_proxy import Proxy


class Foo(object):
    def __init__(self):
        self.foo = 4

    def bar(self):
        return 5 * self.foo


def test():
    foo = Foo()
    proxy = Proxy(foo)

    print proxy.foo
    print proxy.bar()


if __name__ == "__main__":
    test()
