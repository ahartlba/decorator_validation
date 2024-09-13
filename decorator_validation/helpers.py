import inspect
from typing import Callable, Tuple, Union, Any
from .types import SkipTypeCheck


class Validator:
    """Class that handles type validation of non-default annotations"""

    TYPECHECK = 0
    CALLABLE_CHECK = 1

    def __init__(self, validator: Union[type, Tuple[type], Callable[[Any], bool]]):
        """initialize validator

        Parameters
        ----------
        validator : Union[Tuple[type], Callable[[Any], bool]]
            tuple of possible types (like int, float, str, ...) or callable that verifies correctness of type
        """
        if isinstance(validator, type):
            validator = (validator,)
        self.validator = validator

    def validate(self, input) -> Tuple[int, bool]:
        if isinstance(self.validator, tuple):
            type_of_check = self.TYPECHECK
            valid = SkipTypeCheck in self.validator or isinstance(input, self.validator)
        else:
            type_of_check = self.CALLABLE_CHECK
            valid = True
            if self.validator is None:
                valid = True
            else:
                valid = self.validator(input)
        return type_of_check, valid


class Annotation:
    """annotation class handles typecheck for a type-annotation"""

    OVERRIDE = 0
    SIGNATURE = 1

    def __init__(self, annotation, type_):
        """instantiate annotation

        Parameters
        ----------
        annotation : any
            the used annotation in the header or override, can also be a validator
        type : int
            Either Annotation.OVERRIDE or Annotation.SIGNATURE
        """
        self.annotation = annotation
        self.type = type_

    def matches(self, arg) -> bool:
        if self.type == Annotation.SIGNATURE:
            # in case of default signature: check if type matches annotation
            # in case of no annotation -> ok
            return self.annotation == inspect._empty or isinstance(arg, self.annotation)
        elif self.type == Annotation.OVERRIDE:
            # when override create validator object
            #
            validator = Validator(self.annotation)
            type_of_check, res = validator.validate(arg)

            # allow single typing
            if  isinstance(self.annotation, type):
                self.annotation = (self.annotation,)

            if type_of_check == Validator.TYPECHECK and SkipTypeCheck in self.annotation:
                return True
            return res
