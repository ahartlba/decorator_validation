from typing import Callable, Any, Union


class ValidationError(Exception):
    ...


class SkipTypeCheck(type):
    ...


NoneType = type(None)

ValidatorType = Callable[[Any], bool]

Number = Union[int, float]
