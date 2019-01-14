
__author__ = "Sanju Sci"
__email__ = "sanju.sci9@gmail.com"
__copyright__ = "Copyright 2019."

import importlib


def load_class(fully_qualified_class_name):
    """
    Dynamically loads/imports a class by it's fully qualified name.

    Note - It returns class **type**, NOT the instance of class.

    Usage -
            `my_class = load_class('my_package.my_module.MyClass')`

            `my_class_obj = my_class()`

    """
    class_data = fully_qualified_class_name.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = importlib.import_module(module_path)
    # Finally, we retrieve the Class
    return getattr(module, class_str)


def get_fully_qualified_classname(cls=None, obj=None):
    """
    Returns `fully-qualified-name` of the class represented by **cls** or **obj**

    :param cls:
    :param obj:
    :return:
    """
    if obj:
        module = obj.__class__.__module__
        if module is None or module == str.__class__.__module__:
            return obj.__class__.__name__
        return module + '.' + obj.__class__.__name__
    elif cls:
        module = cls.__module__
        if module is None or module == str.__class__.__module__:
            return cls.__name__
        return module + '.' + cls.__name__


def safe_invoke(func, *args, on_success=None, on_error=None, **kwargs):
    res = None
    try:
        res = func(*args, **kwargs)
        if on_success: on_success(res)
    except Exception as ex:
        # Any uncaught exception will be handled here.
        import traceback
        print("Non-standard error occurred!")
        print(traceback.format_exc())
        if on_error: on_error(ex)
    return res
