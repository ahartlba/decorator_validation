import unittest
from typing import List, Dict
from decorator_validation.decorators import validate
from decorator_validation.types import SkipTypeCheck, Number
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

        @validate(custom_validation)
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

        @validate(custom_validation)
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

        @validate(custom_validation)
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            worked = foo(bar=3.2, message="some string", some_additional_info=dict())
        except Exception as e:
            logging.error(e)
        self.assertEqual(worked, True)

    def test_mix_types_functions(self):
        @validate(bar=(SkipTypeCheck,), message=lambda x: isinstance(x, str), some_additional_info=(dict,))
        def foo(bar: Number, message: str, some_additional_info: dict):
            return True

        try:
            _ = foo(dict(bar="also string", message=bytes("some bytes"), some_additional_info=dict()))
        except TypeError:
            worked = True
        else:
            worked = False
        self.assertEqual(worked, True)

    def test_list_of_numbers(self):
        @validate(
            list_1=lambda x: all([isinstance(y, (int, float)) for y in x]),
            list_2=lambda x: all([isinstance(y, (int, float)) for y in x]),
        )
        def foo(list_1: List[Number], list_2: List[Number]):
            return True

        try:
            worked = foo([1, 2, 3], [4, 5, 6])
        except Exception:
            worked = False
        self.assertEqual(worked, True)

    def test_list_of_numbers_incorrect(self):
        @validate(
            list_1=lambda x: all([isinstance(y, (int, float)) for y in x]),
            list_2=lambda x: all([isinstance(y, (int, float)) for y in x]),
        )
        def foo(list_1: List[Number], list_2: List[Number]):
            return True

        try:
            worked = foo([1, 2, "hello"], [4, 5, 6])
        except Exception:
            worked = False
        self.assertNotEqual(worked, True)


if __name__ == "__main__":
    unittest.main()
