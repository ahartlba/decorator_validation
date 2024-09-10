from typing import Union, Tuple, Iterable, Sequence
from pathlib import Path
from .decorators import make_validator


@make_validator
def is_file(file: Union[str, Path]) -> None:
    """check if file is a file"""
    if not Path(file).resolve().is_file():
        raise TypeError(f"File {file} does not exist!")


def is_iterable_of(type_: Union[type, Tuple[type]]):
    @make_validator
    def check_fn(arg: Iterable):
        if not isinstance(arg, Iterable):
            raise TypeError("Argument has to be an iterable!")
        for a in arg:
            if not isinstance(a, type_):
                raise TypeError(
                    f"Argument has to be an iterable with elements of type {type_},\
                          but an element with type {type(a)} occured"
                )

    return check_fn


def is_sequence_of(type_: Union[type, Tuple[type]]):
    @make_validator
    def check_fn(arg: Sequence):
        if not isinstance(arg, Sequence):
            raise TypeError("Argument has to be an iterable!")
        for a in arg:
            if not isinstance(a, type_):
                raise TypeError(
                    f"Argument has to be a sequence with elements of type {type_},\
                          but an element with type {type(a)} occured"
                )

    return check_fn


@make_validator
def is_num_as_str(number: str):
    if not isinstance(number, str):
        raise TypeError(f"{number} is not of type str but of type {type(number)}")
    float(number)  # fails if not possible
