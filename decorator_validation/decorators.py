from typing import Callable, Tuple, Optional, Dict, Union, Any
from functools import wraps
from decorator_validation.types import ValidationError, SkipTypeCheck, ValidatorType
import inspect


class Validator:
    TYPECHECK = 0
    CALLABLE_CHECK = 1

    def __init__(self, validator: Union[Tuple, Callable]):
        self.validator = validator

    def validate(self, input):
        if isinstance(self.validator, tuple):
            return self.TYPECHECK, SkipTypeCheck in self.validator or isinstance(input, self.validator)
        else:
            if self.validator is None:
                return self.CALLABLE_CHECK, True
            return self.CALLABLE_CHECK, self.validator(input)


def convert_with(converter: Callable[[Any], Tuple[Tuple, Dict]]):
    # fmt: off
    def inner(func):
        @wraps(func)
        def inner_inner(*args, **kwargs):
            new_args, new_kwargs = converter(*args, **kwargs)
            return func(*new_args, **new_kwargs)
        return inner_inner
    return inner


def validate_with(validator: ValidatorType):
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


def validate_map(
    *validators: ValidatorType,
    unpacked_arg_validators: Optional[Union[ValidatorType, None]] = None,
    **validator_kwargs: Dict[str, ValidatorType],
):
    """decorator for fast one-level type-checking

    Parameters
    ----------
    types: tuple
        tuple of allowed types in function
    unpacked_arg_types : tuple | None, optional
        types for arguments that come from unpack-operator, by default None
    type_kwargs

    Raises
    ------
    ValidationError
        if validation did not succeed for any input
    """

    def inner(func):
        @wraps(func)
        def inner_inner(*args, **kwargs):
            def always_true(x):
                return True

            if unpacked_arg_validators:
                zip_ = zip(validators + (unpacked_arg_validators,) * (len(args) - len(validators)), args)
            else:
                zip_ = zip(validators + tuple(validator_kwargs.values()), args)
            for validator, arg in zip_:
                if validator is None:
                    validator = always_true
                if not validator(arg):
                    raise ValidationError(f"Validation failed ValidationError for arg{arg} with {validator.__name__}")
            for key, val in kwargs.items():
                validator = validator_kwargs[key]
                if validator is None:
                    validator = always_true
                if not validator(val):
                    raise ValidationError(f"Validation failed for parameter {key} with {validator.__name__}")
            return func(*args, **kwargs)

        return inner_inner

    return inner


def validate(
    *validators: Union[ValidatorType, Dict],
    unpacked_arg_validators: Optional[Union[ValidatorType, None]] = None,
    **validator_kwargs: Dict[str, ValidatorType],
):
    """decorator for fast one-level type-checking

    Parameters
    ----------
    types: tuple
        tuple of allowed types in function
    unpacked_arg_types : tuple | None, optional
        types for arguments that come from unpack-operator, by default None
    type_kwargs

    Raises
    ------
    ValidationError
        if validation did not succeed for any input
    """

    def inner(func):
        if len(validators) == 1 and not unpacked_arg_validators and not validator_kwargs:

            @wraps(func)
            def inner_inner(*args, **kwargs):
                if validators[0](*args, **kwargs):
                    return func(*args, **kwargs)
                raise ValidationError("Something went wrong")

            return inner_inner

        @wraps(func)
        def inner_inner(*args, **kwargs):
            if unpacked_arg_validators:
                zip_ = zip(validators + (unpacked_arg_validators,) * (len(args) - len(validators)), args)
            else:
                zip_ = zip(validators + tuple(validator_kwargs.values()), args)
            for validation_obj, arg in zip_:
                validator = Validator(validation_obj)
                type_of_check, res = validator.validate(arg)
                if not res:
                    if type_of_check == Validator.TYPECHECK:
                        allowed_types = validation_obj
                        if SkipTypeCheck not in allowed_types and not isinstance(arg, allowed_types):
                            raise TypeError(f"Type Mismatch {type(arg)} not in {allowed_types}")
                    else:
                        if not validation_obj(arg):
                            raise ValidationError(
                                f"Validation failed ValidationError for arg{arg} with {validation_obj.__name__}"
                            )
            for key, val in kwargs.items():
                validation_obj = validator_kwargs[key]
                validator = Validator(validation_obj)
                type_of_check, res = validator.validate(val)
                if not res:
                    if type_of_check == Validator.TYPECHECK:
                        allowed_types = validation_obj
                        if SkipTypeCheck not in allowed_types and not isinstance(arg, allowed_types):
                            raise TypeError(f"Type Mismatch {type(arg)} not in {allowed_types}")
                    else:
                        if not validation_obj(val):
                            raise ValidationError(
                                f"Validation failed ValidationError for arg{key} with {validation_obj.__name__}"
                            )
            return func(*args, **kwargs)

        return inner_inner

    return inner


class Annotation:
    OVERRIDE = 0
    SIGNATURE = 1

    def __init__(self, annotation, type):
        self.annotation = annotation
        self.type = type

    def type_error_occured(self, input) -> bool:
        if self.type == Annotation.SIGNATURE:
            return not self.annotation == inspect._empty and not isinstance(input, self.annotation)
        elif self.type == Annotation.OVERRIDE:
            validator = Validator(self.annotation)
            type_of_check, res = validator.validate(input)
            if type_of_check == Validator.TYPECHECK:
                if SkipTypeCheck in self.annotation:  # ignore result for SkipTypeCheck
                    return False
                return not res
            return not res


def check_types(**override_kwargs):
    def inner(func):
        @wraps(func)
        def inner_inner(*args, **kwargs):
            _signature = inspect.signature(func)
            for i, (param, arg) in enumerate(zip(_signature.parameters.values(), args)):
                try:
                    override = override_kwargs[param.name]
                except KeyError:
                    override = None
                annotation = (
                    Annotation(param.annotation, Annotation.SIGNATURE)
                    if not override
                    else Annotation(override, Annotation.OVERRIDE)
                )
                if annotation.type_error_occured(arg):
                    raise TypeError(
                        f"TypeError for Parameter {param.name}: input_type: {type(arg)}: required: {param.annotation}"
                    )
            for k, v in kwargs.items():
                annotation = (
                    Annotation(_signature.parameters[k].annotation, Annotation.SIGNATURE)
                    if k not in override_kwargs
                    else Annotation(override_kwargs[k], Annotation.OVERRIDE)
                )
                if annotation.type_error_occured(v):
                    raise TypeError(
                        f"TypeError for Parameter {param.name}: input_type: {type(v)}: required: {param.annotation}"
                    )
            return func(*args, **kwargs)

        return inner_inner

    return inner
