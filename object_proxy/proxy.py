class Proxy(object):
    """
    A proxy to an object.
    Any action performed on the proxy will be done on the original object,
    and the result will be given back to the user.
    """

    ATTRIBUTES_TO_COPY_FROM_TYPE = [
        "__name__",
        "__doc__",
    ]

    @staticmethod
    def __set_from_type(obj, proxy_class):
        """
        Sets attributes of the class of the proxy object
        to the appropriate attributes of the class of the original object.
        :param obj: The original object.
        :type obj: object
        :param proxy_class: The class of the proxy object.
        :type proxy_class: type
        """
        for attr_to_copy in Proxy.ATTRIBUTES_TO_COPY_FROM_TYPE:
            attr = getattr(type(obj), attr_to_copy)
            setattr(proxy_class, attr_to_copy, attr)

    @staticmethod
    def __set_special_methods(obj, proxy_class):
        """
        Sets special `__methods__` of the proxy class
        to call the appropriate method of the original object.
        :param obj: The original object.
        :type obj: object
        :param proxy_class: The class of the proxy object.
        :type proxy_class: type
        """
        for attribute_name, attribute in type(obj).__dict__.items():
            if not callable(getattr(obj, attribute_name)):
                continue

            def get_wrapped_attribute(attr_name):
                def wrapped_attribute(_self, *args, **kwargs):
                    return getattr(obj, attr_name)(*args, **kwargs)
                return wrapped_attribute

            setattr(proxy_class, attribute_name, get_wrapped_attribute(attribute_name))

    def __new__(cls, obj):
        """
        Create a new proxy object.
        This dynamically creates a class for the new proxy and sets
        all the necessary attributes and methods to the class before initializing it.
        :param obj: The original object to create a proxy to.
        :type obj: object
        :return: A new proxy object.
        :rtype: type(obj)
        """
        class _Proxy(object):
            def __getattr__(self, item):
                return getattr(obj, item)

        cls.__set_from_type(obj, _Proxy)
        cls.__set_special_methods(obj, _Proxy)

        return _Proxy()
