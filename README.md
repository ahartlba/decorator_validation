# Validation Decorators

![Unittest](https://github.com/ahartlba/decorator_validation/actions/workflows/testing.yml/badge.svg?branch=main)
![Static Badge](https://img.shields.io/badge/https%3A%2F%2Fimg.shields.io%2Fbadge%2Fcode%2520style-black-black?label=codestyle)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/decorator-validation)

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
@validate_types(bar=(int,), message=(str,), some_additional_info=(dict,))
def foo(bar: int, message: str, some_additional_info: dict):
    # begin to code
```

If of course also supports multiple types:

```python
from pathlib import Path

@validate_types(path=(str, Path), message=(str,))
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

Skip Type-checks by providing the `SkipTypecheck` class as a type, this is very usefull for methods.

```python
from decorator_validation.decorators import validate_types
from decorator_validation.types import SkipTypeCheck

class FileReader:

    @validate_types((SkipTypeCheck,), file_path=(str,))
    def __init__(self, file_path: str):
        ...

```

Of course, sometimes you want to have custom error messages.
Then, just use the following code:

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

```python

from decorator_validation.decorators import validate_map
from decorator_validation.std_validators import is_file

class FileReader:

    @validate_map(None, file_path=is_file)
    def __init__(self, file_path: str):
        ...

```

## Validate Arbitrary Arguments

Starting with version `2.0.0`, the package allows for a single use decorator called `validate`.

Depending on the argument, it will either check the type or use a function to validate.
If a tuple is used, the standard typecheck will be applied, if not it expectes a Callable that returns a boolean value.
All of the examples above can be directly copied and just the name of the decorator has to be changed.

An example.

```python

from decorator_validation.decorators import validate
from decorator_validation.std_validators import is_file

class Logger:

    @validate(file_path=is_file, message=(str,))
    def log(file_path: str, message:str):
        ...

```
