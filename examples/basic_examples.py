from decorator_validation import check_types

# check the types of your function


@check_types
def foo(a: int, b: int):
    return a * b


foo(2, 2, 3.3)  # returns 6
foo(2.0, 3)  # raises TypeError as argument a has no correct type

# to overwrite args pass in key mappings to the decorator.
# Types have to be wrapped with a tuple


@check_types(b=(int, float))
def foo(a: int, b: int):
    return a * b


foo(2, 3)  # returns 6
foo(2, 3.0)  # returns 6.0
foo(2.0, 3)  # raises typeerror

# You can also use functions to validate certain inputs

from decorator_validation.std_validators import is_file


@check_types(file=is_file)
def write_to_file(file: str, text: str): ...


write_to_file("non_existing_file.txt", "hello file")  # will raise a type-error if file does not exist.

# You can also define custom "validators". Just make sure the function takes in the function input as an argument
# and returns True if it is valid. In case it is'nt, raise an exception with a custom message or return False.


def is_divisible_by_10(number: int | float):
    return number % 10 == 0


# recommended version would use exceptions though for a more readable error msg
def is_divisible_by_10_better(number: int | float):
    if not number % 10 == 0:
        raise ValueError("Input Argument is not divisible by 10")
    return True


# for the above example you can use the utility decorator to make the code even more concise
from decorator_validation import make_validator


@make_validator
def is_divisible_by_10_best(number: int | float):
    if not number % 10 == 0:
        raise ValueError("Input Argument is not divisible by 10")
