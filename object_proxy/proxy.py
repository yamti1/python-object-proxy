class Proxy(object):
    COPY_FROM_TYPE = [
        "__name__",
        "__doc__",
    ]

    @staticmethod
    def __copy_from_type(obj, proxy_class):
        for attr_to_copy in Proxy.COPY_FROM_TYPE:
            attr = getattr(type(obj), attr_to_copy)
            setattr(proxy_class, attr_to_copy, attr)

    @staticmethod
    def __set_special_methods(obj, proxy_class):
        for attribute_name, attribute in type(obj).__dict__.items():
            if not callable(getattr(obj, attribute_name)):
                continue

            def get_wrapped_attribute(attr_name):
                def wrapped_attribute(_self, *args, **kwargs):
                    return getattr(obj, attr_name)(*args, **kwargs)
                return wrapped_attribute

            setattr(proxy_class, attribute_name, get_wrapped_attribute(attribute_name))

    def __new__(cls, obj):
        class _Proxy(object):
            def __getattr__(self, item):
                return getattr(obj, item)

        cls.__copy_from_type(obj, _Proxy)
        cls.__set_special_methods(obj, _Proxy)

        return _Proxy()
