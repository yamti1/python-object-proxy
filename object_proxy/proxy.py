class Proxy(object):
    """
    A proxy to an object.
    Any action performed on the proxy will be done on the original object,
    and the result will be given back to the user.
    """

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

    @staticmethod
    def __set_attribute_access(obj, proxy_class):
        """
        Sets `__getattr__`, `__setattr__` and `__delattr__` of the proxy class
        to delegate the calls to the original object.
        :param obj: The original object.
        :type obj: object
        :param proxy_class: The class of the proxy object.
        :type proxy_class: type
        """
        def get_attribute(_proxy, attribute_name):
            return getattr(obj, attribute_name)

        def set_attribute(_proxy, attribute_name, value):
            return setattr(obj, attribute_name, value)

        def del_attribute(_proxy, attribute_name):
            return delattr(obj, attribute_name)

        funcs_map = {
            "__getattr__": get_attribute,
            "__setattr__": set_attribute,
            "__delattr__": del_attribute,
        }

        for func_name, func in funcs_map.items():
            setattr(proxy_class, func_name, func)

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

        # Create a class copy
        class_dict = dict(type(obj).__dict__)
        class_name = type(obj).__name__
        class_bases = type(obj).__bases__

        _Proxy = type(class_name, class_bases, class_dict)

        cls.__set_special_methods(obj, _Proxy)
        cls.__set_attribute_access(obj, _Proxy)

        return _Proxy()


