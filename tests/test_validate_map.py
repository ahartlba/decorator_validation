import unittest
from typing import Dict
from decorator_validation.decorators import validate_map
from decorator_validation.types import ValidationError
import logging


class TestValidateMap(unittest.TestCase):
    def test_correct(self):
        def divisible_by_10(x):
            return x % 10 == 0

        @validate_map(bar=divisible_by_10, message=lambda x: isinstance(x, str), some_additional_info=None)
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            worked = foo(bar=20, message="some string", some_additional_info=dict())
        except ValidationError as e:
            logging.error(e)
            worked = False
        self.assertEqual(worked, True)

    def test_only_args_correct(self):
        def divisible_by_10(x):
            return x % 10 == 0

        @validate_map(bar=divisible_by_10, message=lambda x: isinstance(x, str), some_additional_info=None)
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            worked = foo(20, "some string", dict())
        except ValidationError as e:
            logging.error(e)
            worked = False
        self.assertEqual(worked, True)

    def test_only_args_kwargs_mix_correct(self):
        def divisible_by_10(x):
            return x % 10 == 0

        @validate_map(bar=divisible_by_10, message=lambda x: isinstance(x, str), some_additional_info=None)
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            worked = foo(20, some_additional_info=dict(), message="some string")
        except ValidationError as e:
            logging.error(e)
            worked = False
        self.assertEqual(worked, True)

    def test_not_correct(self):
        def divisible_by_10(x):
            return x % 10 == 0

        @validate_map(bar=divisible_by_10, message=lambda x: isinstance(x, str), some_additional_info=lambda x: True)
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            worked = foo(bar=2, message="some string", some_additional_info=dict())
        except ValidationError as e:
            logging.error(e)
            worked = False
        self.assertNotEqual(worked, True)

    def test_none(self):
        def divisible_by_10(x):
            return x % 10 == 0

        @validate_map(bar=divisible_by_10, message=None, some_additional_info=None)
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            worked = foo(20, some_additional_info=dict(), message=43)
        except ValidationError as e:
            logging.error(e)
            worked = False
        self.assertEqual(worked, True)


if __name__ == "__main__":
    unittest.main()
