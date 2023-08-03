from typing import Callable, Tuple, Optional, Dict, Union
from functools import wraps


class ValidationError(Exception):
    ...


class SkipTypeCheck(type):
    ...


def convert_with(converter: Callable):
    # fmt: off
    def inner(func):
        @wraps(func)
        def inner_inner(*args, **kwargs):
            new_args, new_kwargs = converter(*args, **kwargs)
            return func(*new_args, **new_kwargs)
        return inner_inner
    return inner


def validate_with(validator: Callable):
    """Decorator that validates args and kwargs passed to the decorated function with the validator.

    The Validator has to return either 0, None or False, or directly throw an exception.

    Parameters
    ----------
    validator : Callable
        validation function that takes in args and kwargs passed to the decorated function

    Raises
    ------
    ValidationError
        if the validation was not successful
    """
    # fmt: off
    def inner(func):
        @wraps(func)
        def inner_inner(*args, **kwargs):
            if validator(*args, **kwargs):
                return func(*args, **kwargs)
            raise ValidationError("Something went wrong")
        return inner_inner
    return inner
    # fmt: on


def validate_types(
    *types: Tuple,
    unpacked_arg_types: Optional[Union[Tuple, None]] = None,
    **type_kwargs: Dict[str, tuple],
):
    """decorator for fast one-level type-checking

    Parameters
    ----------
    types: tuple
        tuple of allowed types in function
    unpacked_arg_types : tuple | None, optional
        types for arguments that come from unpack-operator, by default None
    type_kwargs
    """

    def inner(func):
        @wraps(func)
        def inner_inner(*args, **kwargs):
            if unpacked_arg_types:
                zip_ = zip(types + (unpacked_arg_types,) * (len(args) - len(types)), args)
            else:
                zip_ = zip(types + tuple(type_kwargs.values()), args)
            for allowed_types, arg in zip_:
                if SkipTypeCheck not in allowed_types and not isinstance(arg, allowed_types):
                    raise TypeError(f"Type Mismatch {type(arg)} not in {allowed_types}")
            for key, val in kwargs.items():
                allowed_types = type_kwargs[key]
                if SkipTypeCheck not in allowed_types and not isinstance(val, allowed_types):
                    raise TypeError(f"Type Mismatch {type(val)} not in {allowed_types}")
            return func(*args, **kwargs)

        return inner_inner

    return inner
