from functools import wraps
from typing import Callable, Any
import inspect
from .helpers import Annotation


class check_types:
    """Decorator to automatically check input types of a function based on type annotation"""

    def __new__(cls, func=None, **kwargs):
        # support for @check_types instead of @check_types()
        if func is not None:
            instance = super().__new__(cls, **kwargs)
            instance._override_kwargs = kwargs
            return instance(func)
        return super().__new__(cls)

    def __init__(self, **override_kwargs):
        self._override_kwargs = override_kwargs

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            _signature = inspect.signature(func)

            # check all arguments
            for param, arg in zip(_signature.parameters.values(), args):
                # check if an override occured for the parameter
                override = self._override_kwargs.get(param.name, None)

                if not override:
                    annotation = Annotation(param.annotation, Annotation.SIGNATURE)  # default signature
                else:
                    annotation = Annotation(override, Annotation.OVERRIDE)  # override instead of signature

                # type does not match the annotation
                if annotation.type_error_occured(arg):
                    raise TypeError(
                        f"TypeError for Parameter {param.name}: input_type: {type(arg)}: required: {param.annotation}"
                    )

            # check all kwargs
            for k, v in kwargs.items():
                if k not in self._override_kwargs:
                    annotation = Annotation(_signature.parameters[k].annotation, Annotation.SIGNATURE)
                else:
                    annotation = Annotation(self._override_kwargs[k], Annotation.OVERRIDE)

                # type does not match the annotation
                if annotation.type_error_occured(v):
                    raise TypeError(
                        f"TypeError for Parameter {k}: input_type: {type(v)}: required: {annotation.annotation}\nMake sure your custom validator did not fail if you used one!"
                    )
            return func(*args, **kwargs)

        return inner


def make_validator(func: Callable[[Any], None]) -> Callable[[Any], bool]:
    """takes in function that raises error for wrong type and makes it return
    True if no exception occurs"""

    @wraps(func)
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        return True

    return inner
