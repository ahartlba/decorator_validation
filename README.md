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
def foo(bar: int, message: str):
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