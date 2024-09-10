# Validation Decorators

![Unittest](https://github.com/ahartlba/decorator_validation/actions/workflows/testing.yml/badge.svg?branch=main)
![Static Badge](https://img.shields.io/badge/https%3A%2F%2Fimg.shields.io%2Fbadge%2Fcode%2520style-black-black?label=codestyle)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/decorator-validation)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)

Simple and fast type-checking and parameter validation.

Install with

```bash
pip install decorator-validation
```

## Why?

Do you want to remove visual clutter in your python function?
Do you want to check types fast without a lot of boilerplate?

Then this package is right for you.

Not convinced? Check out the following:

```python
# classic
def foo(bar: int, message: str, some_additional_info: dict):
    if not isinstance(bar, int):
        raise TypeError(...)
    if not isinstance(message, str):
        raise TypeError(...)
    if not isinstance(some_additional_info, dict):
        raise TypeError(...)
    # now begin to code...

# now
from decorator_validation import check_types

@check_types
def foo(bar: int, message: str, some_additional_info: dict):
    # begin to code
```

Checkout the codebase for more examples and built in decorators!

> **NOTE**: `check_types` has limitations for python versions lower than 3.10 due to lack of built in language support for type-checking. Use with caution with special types and None-Types!

## More Example

Of course, sometimes you want to have a custom validation method for all your inputs.
It just needs to return if the input is valid or not.

```python
from decorator_validation import check_types
from pathlib import Path

def my_validation_func(file_path:str) -> True:

    if not isinstance(file_path, str):
        raise TypeError(...)
    if not Path(file_path).resolve().is_file():
        raise ValueError(...)
    return True

class FileReader:

    @check_types(file_path=my_validation_func)
    def __init__(self, file_path: str):
        ...

```

## Default Validators

This Repository comes with its own default validation functions, like if an input is a valid file.
A Validation function is a function that returns `True` of `False` (or raises an exception) if the input is correct / incorrect.

```python

from decorator_validation import check_types
from decorator_validation.std_validators import is_file

class FileReader:

    @check_types(file_path=is_file)
    def __init__(self, file_path: str):
        ...

```

## Validate Arbitrary Arguments

You can of course combine validation functions with type-check-skipping and the
signature_usage.
SkipTypeCheck can be used for non-supported types in type-hinting etc.

```python

from decorator_validation import check_types, SkipTypeCheck
from decorator_validation.std_validators import is_file

class Logger:

    @check_types(file_path=is_file, message=(SkipTypeCheck,))
    def log(file_path: str, message: str, repeat: int = 1):
        ...

    log('some_file.txt', 'hello')  # works
    log('some_file.txt', 2)  # works
    log('some_file.txt', 2, '3')  # does not work

```
