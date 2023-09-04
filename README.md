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
@check_types()
def foo(bar: int, message: str, some_additional_info: dict):
    # begin to code
```

Checkout the codebase for more examples and built in decorators!

> **NOTE**: `check_types` has limitations for python versions lower than 3.10 due to lack of built in language support for type-checking. Use with caution with special types and None-Types!

## More Examples

> **Note**: `check_types` is only available since release 2.2.0. for previous releases checkout `validate_types`. For more details check out the repository and older releases :).

If of course also supports multiple types:

```python
from pathlib import Path

@check_types()
def foo(path: str | Path, message: str):
    # begin to code
```

Do you want to convert your input-types fast and without clutter?

```python
def from_dict(dict_: dict):
    return (dict_.get('bar'), dict_.get('message'), dict_.get('some_additional_info')), {}

@convert_with(from_dict)
def foo(bar: int, message:str, some_additional_info: dict):
    ...

```

Skip Type-checks by providing the `SkipTypecheck` class as a type. This enables you
to skip the type check even if you have type-annotations.
This is usefull if you do not wont to check some stuff but want to use the type-hints

```python
from decorator_validation.decorators import validate_types
from decorator_validation.types import SkipTypeCheck

class FileReader:

    @check_types(self=(SkipTypeCheck,), file_path=(str,))
    def __init__(self, file_path: str):
        ...

```

Of course, sometimes you want to have a custom validation method for all your inputs.
Then, just use the `validate_with` function.

```python
from decorator_validation.decorators import validate_with
from pathlib import Path

def my_validation_func(obj, file_path:str) -> True:

    if not isinstance(file_path, str):
        raise TypeError(...)
    if not Path(file_path).resolve().is_file():
        raise ValueError(...)
    return True

class FileReader:

    @validate_with(my_validation_func)
    def __init__(self, file_path: str):
        ...

```

## Map Multiple functions for subtypes

You can also directly map different validation functions to your arguments.
A Validation function is a function that returns `True` of `False` (or raises an exception) if the input is correct / incorrect.

```python

from decorator_validation.decorators import check_types
from decorator_validation.std_validators import is_file

class FileReader:

    @check_types(file_path=is_file)
    def __init__(self, file_path: str):
        ...

```

## Validate Arbitrary Arguments

You can of course combine validation functions with type-check-skipping and the
signature_usage.

```python

from decorator_validation.decorators import check_types
from decorator_validation.types import SkipTypeCheck
from decorator_validation.std_validators import is_file

class Logger:

    @check_types(file_path=is_file, message=(SkipTypeCheck,))
    def log(file_path: str, message: str, repeat: int = 1):
        ...

    log('some_file.txt', 'hello')  # works
    log('some_file.txt', 2)  # works
    log('some_file.txt', 2, '3')  # does not work

```
