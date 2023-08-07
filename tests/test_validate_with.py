import unittest
from typing import Dict
from decorator_validation.decorators import validate_with
import logging


class TestConvertWith(unittest.TestCase):
    def test_correct_validator(self):
        def custom_validation(bar: int, message: str, some_additional_info: Dict):
            if not isinstance(bar, int):
                raise TypeError
            if not isinstance(message, str):
                raise TypeError
            if not isinstance(some_additional_info, dict):
                raise TypeError
            return True

        @validate_with(custom_validation)
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            worked = foo(bar=3, message="some string", some_additional_info=dict())
        except Exception as e:
            logging.error(e)
        self.assertEqual(worked, True)

    def test_correct_validator_false_args(self):
        def custom_validation(bar: int, message: str, some_additional_info: Dict):
            if not isinstance(bar, int):
                raise TypeError
            if not isinstance(message, str):
                raise TypeError
            if not isinstance(some_additional_info, dict):
                raise TypeError
            return True

        @validate_with(custom_validation)
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            _ = foo(bar=3.2, message="some string", some_additional_info=dict())
        except Exception:
            worked = True
        else:
            worked = False
        self.assertEqual(worked, True)

    def test_invalid_validator(self):
        def custom_validation(bar: int, message: str, some_additional_info: Dict):
            if not isinstance(bar, float):
                raise TypeError
            if not isinstance(message, str):
                raise TypeError
            if not isinstance(some_additional_info, dict):
                raise TypeError
            return True

        @validate_with(custom_validation)
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            worked = foo(bar=3.2, message="some string", some_additional_info=dict())
        except Exception as e:
            logging.error(e)
        self.assertEqual(worked, True)


if __name__ == "__main__":
    unittest.main()
