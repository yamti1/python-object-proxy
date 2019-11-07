class Proxy(object):
    def __new__(cls, obj):
        class Wrapper(object):
            def __getattr__(self, item):
                return getattr(obj, item)

        for attribute_name, attribute in type(obj).__dict__.items():
            if not callable(getattr(obj, attribute_name)):
                continue

            def get_wrapped_attribute(attr_name):
                def wrapped_attribute(_self, *args, **kwargs):
                    return getattr(obj, attr_name)(*args, **kwargs)
                return wrapped_attribute

            setattr(Wrapper, attribute_name, get_wrapped_attribute(attribute_name))

        return Wrapper()
