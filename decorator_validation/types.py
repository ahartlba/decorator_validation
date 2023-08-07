class ValidationError(Exception):
    ...


class SkipTypeCheck(type):
    ...


NoneType = type(None)
