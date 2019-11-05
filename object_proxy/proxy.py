class Proxy(object):
    def __new__(cls, obj):
        class Wrapper(object):
            def __getattr__(self, item):
                return getattr(obj, item)

        for attribute_name, attribute in type(obj).__dict__.items():
            if not callable(getattr(obj, attribute_name)):
                continue

            def wrapped_attribute(*args, **kwargs):
                getattr(obj, attribute_name)(*args, **kwargs)

            setattr(Wrapper, attribute_name, wrapped_attribute)

        return Wrapper
