# Validation Decorators

Simple and fast type-checking and parameter validation.

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
def foo(bar: int, message: str, , some_additional_info: dict):
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
