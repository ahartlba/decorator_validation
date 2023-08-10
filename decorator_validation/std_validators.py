from typing import Union, Tuple, Iterable, Sequence
from pathlib import Path


def is_file(file: Union[str, Path]) -> bool:
    """check if file is a file"""
    return Path(file).resolve().is_file()


def is_iterable_of(type_: Union[type, Tuple[type]]):
    def check_fn(arg: Iterable):
        if not isinstance(arg, Iterable):
            raise TypeError("Argument has to be an iterable!")
        for a in arg:
            if not isinstance(a, type_):
                raise TypeError(
                    f"Argument has to be an iterable with elements of type {type_},\
                          but an element with type {type(type_)} occured"
                )
        return True

    return check_fn


def is_sequence_of(type_: Union[type, Tuple[type]]):
    def check_fn(arg: Sequence):
        if not isinstance(arg, Sequence):
            raise TypeError("Argument has to be an iterable!")
        for a in arg:
            if not isinstance(a, type_):
                raise TypeError(
                    f"Argument has to be a sequence with elements of type {type_},\
                          but an element with type {type(type_)} occured"
                )
        return True

    return check_fn


def is_num_as_str(number: str):
    if not isinstance(number, str):
        raise TypeError(f"{number} is not of type str but of type {type(number)}")
    try:
        float(number)
        return True
    except Exception:
        return False
