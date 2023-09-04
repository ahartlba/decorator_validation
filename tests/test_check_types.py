import unittest
from typing import Dict, Union, Sequence
from decorator_validation.decorators import check_types
from decorator_validation.types import SkipTypeCheck
from decorator_validation.std_validators import is_sequence_of
import logging
import platform


class TestCheckTypes(unittest.TestCase):
    def test_correct_types_only_kwargs(self):
        @check_types()
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            worked = foo(bar=3, message="some string", some_additional_info=dict())
        except Exception as e:
            worked = False
            logging.error(e)
        self.assertEqual(worked, True)

    def test_correct_types_only_args(self):
        @check_types()
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            worked = foo(3, "some string", dict())
        except Exception as e:
            worked = False
            logging.error(e)
        self.assertEqual(worked, True)

    def test_correct_types_mix_args_kwargs(self):
        @check_types()
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
        @check_types()
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            _ = foo(dict(bar=3.2, message="some string", some_additional_info=dict()))
        except TypeError:
            worked = True
        else:
            worked = False
        self.assertEqual(worked, True)

    def test_union_types(self):
        @check_types()
        def foo(bar: Union[int, float], message: Union[str, bytes], some_additional_info: dict):
            return True

        try:
            _ = foo(dict(bar=3.2, message="some string", some_additional_info=dict()))
            _ = foo(dict(bar=3, message=bytes("some bytes"), some_additional_info=dict()))
        except TypeError:
            worked = True
        else:
            worked = False
        self.assertEqual(worked, True)

    def test_skip_type_check(self):
        @check_types()
        def foo(bar: Union[int, float], message: Union[str, bytes], some_additional_info: dict):
            return True

        try:
            _ = foo(dict(bar="also string", message=bytes("some bytes"), some_additional_info=dict()))
        except TypeError:
            worked = True
        else:
            worked = False
        self.assertEqual(worked, True)

    def test_cls_and_obj_stuff(self):
        class Test:
            @check_types()
            def __init__(self, k: int):
                pass

            @classmethod
            @check_types()
            def from_stuff(cls, k: int):
                pass

        Test(1)
        Test.from_stuff(1)

    def test_none(self):
        @check_types()
        def none_test(a: Union[None, str] = None):
            print(a)

        none_test
        if int(platform.python_version().split(".")[1]) > 9:
            none_test(None)
        try:
            none_test(1)
            assert False
        except TypeError:
            assert True

    def test_notype(self):
        @check_types()
        def foo(bar):
            print(bar)

        foo(1)
        foo("str")

    def test_other_types(self):
        @check_types(bar=(SkipTypeCheck,))
        def print_elmnts(bar: Sequence[int]):
            for b in bar:
                ...
            return True

        @check_types(bar=is_sequence_of(int))
        def print_elmnts_2(bar: Sequence[int]):
            for b in bar:
                ...
            return True

        @check_types()
        def print_elmnts_3(bar):
            for b in bar:
                ...
            return True

        print_elmnts([1, 2])
        print_elmnts_2([1, 2])
        print_elmnts_3([1, 2, 'str'])


if __name__ == "__main__":
    unittest.main()
