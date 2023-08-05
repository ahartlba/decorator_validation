import unittest
from typing import Dict, Union
from decorator_validation.decorators import validate_types
from decorator_validation import SkipTypeCheck
import logging


class TestConvertWith(unittest.TestCase):
    def test_correct_types_only_kwargs(self):
        @validate_types(bar=(int,), message=(str,), some_additional_info=(dict,))
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            worked = foo(bar=3, message="some string", some_additional_info=dict())
        except Exception as e:
            logging.error(e)
        self.assertEqual(worked, True)

    def test_correct_types_only_args(self):
        @validate_types(bar=(int,), message=(str,), some_additional_info=(dict,))
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            worked = foo(3, "some string", dict())
        except Exception as e:
            worked = False
            logging.error(e)
        self.assertEqual(worked, True)

    def test_correct_types_mix_args_kwargs(self):
        @validate_types(bar=(int,), message=(str,), some_additional_info=(dict,))
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            worked = foo(
                3,
                some_additional_info=dict(),
                message="some string",
            )
        except Exception as e:
            logging.error(e)
        self.assertEqual(worked, True)

    def test_uncorrect_types(self):
        @validate_types(bar=(int,), message=(str,), some_additional_info=(dict,))
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            _ = foo(dict(bar=3.2, message="some string", some_additional_info=dict()))
        except TypeError as e:
            worked = True
        else:
            worked = False
        self.assertEqual(worked, True)

    def test_union_types(self):
        @validate_types(bar=(int, float), message=(str, bytes), some_additional_info=(dict,))
        def foo(bar: Union[int, float], message: Union[str, bytes], some_additional_info: dict):
            return True

        try:
            _ = foo(dict(bar=3.2, message="some string", some_additional_info=dict()))
            _ = foo(dict(bar=3, message=bytes("some bytes"), some_additional_info=dict()))
        except TypeError as e:
            worked = True
        else:
            worked = False
        self.assertEqual(worked, True)

    def test_skip_type_check(self):
        @validate_types(bar=(SkipTypeCheck,), message=(str, bytes), some_additional_info=(dict,))
        def foo(bar: Union[int, float], message: Union[str, bytes], some_additional_info: dict):
            return True

        try:
            _ = foo(dict(bar="also string", message=bytes("some bytes"), some_additional_info=dict()))
        except TypeError as e:
            worked = True
        else:
            worked = False
        self.assertEqual(worked, True)


if __name__ == "__main__":
    unittest.main()
