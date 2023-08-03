import unittest
from typing import Dict
from decorator_validation.decorators import convert_with
import logging


class TestConvertWith(unittest.TestCase):
    def test_correct_converter(self):
        def from_dict(dict_: Dict):
            return (dict_.get("bar"), dict_.get("message"), dict_.get("some_additional_info")), {}

        @convert_with(from_dict)
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            worked = foo(dict(bar=3, message="some string", some_additional_info=dict()))
        except Exception as e:
            logging.error(e)
        self.assertEqual(worked, True)

    def test_uncorrect_converter(self):
        def from_dict(dict_: Dict):
            return (dict_.get("bar"), dict_.get("message"), dict_.get("some_additional_info"))

        @convert_with(from_dict)
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            _ = foo(dict(bar=3, message="some string", some_additional_info=dict()))
        except Exception as e:
            raised_error = True
        else:
            raised_error = False
        self.assertEqual(raised_error, True)


if __name__ == "__main__":
    unittest.main()
