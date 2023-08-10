import unittest
from decorator_validation.decorators import validate_map, validate
from decorator_validation.std_validators import is_file, is_iterable_of, is_sequence_of, is_num_as_str
from decorator_validation.types import ValidationError
import logging
from pathlib import Path
from typing import Iterable, Union, Sequence


class TempFile:
    def __init__(self, name: str):
        self.name = Path(name)

    def __enter__(self):
        return self

    def write(self, text: str):
        with open(self.name, "a+") as f:
            f.write(text)

    def __exit__(self, *args):
        self.name.unlink()


class TestStandardValidations(unittest.TestCase):
    def test_is_file_correct(self):
        @validate_map(file=is_file)
        def foo(file: str):
            return True

        with TempFile("test.txt") as temp:
            temp.write("hello")
            try:
                worked = foo(file="test.txt")
            except ValidationError as e:
                logging.error(e)
                worked = False
        self.assertEqual(worked, True)

    def test_is_file_not_correct(self):
        @validate_map(file=is_file)
        def foo(file: str):
            return True

        with TempFile("test.txt") as temp:
            temp.write("hello")
            try:
                worked = foo(file="test2.txt")
            except ValidationError as e:
                logging.error(e)
                worked = False
        self.assertNotEqual(worked, True)

    def test_is_iterable_of_correct(self):
        @validate(bar=is_iterable_of(str))
        def foo(bar: Iterable[str]):
            return True

        self.assertEqual(foo(["a", "b", "c"]), True)

        @validate(foo=is_iterable_of((int, float)))
        def bar(foo: Iterable[Union[int, float]]):
            return True

        self.assertEqual(bar((1, 2, 4.3, 3.6)), True)

    def test_is_iterable_of_incorrect(self):
        @validate(bar=is_iterable_of(str))
        def foo(bar: Iterable[str]):
            return True

        result = False
        try:
            result = foo(["a", "b", "c", 3])
        except TypeError:
            TypeError
        self.assertEqual(result, False)

        @validate(foo=is_iterable_of((int, float)))
        def bar(foo: Iterable[Union[int, float]]):
            return True

        result = False
        try:
            result = bar(("a", "b", "c", 3))
        except TypeError:
            TypeError
        self.assertEqual(result, False)

    def test_is_sequence_of_correct(self):
        @validate(bar=is_sequence_of(str))
        def foo(bar: Sequence[str]):
            return True

        self.assertEqual(foo(["a", "b", "c"]), True)

        @validate(foo=is_sequence_of((int, float)))
        def bar(foo: Sequence[Union[int, float]]):
            return True

        self.assertEqual(bar((1, 2, 4.3, 3.6)), True)

    def test_is_sequence_of_incorrect(self):
        @validate(bar=is_sequence_of(str))
        def foo(bar: Sequence[str]):
            return True

        result = False
        try:
            result = foo(["a", "b", "c", 3])
        except TypeError:
            TypeError
        self.assertEqual(result, False)

        @validate(foo=is_sequence_of((int, float)))
        def bar(foo: Sequence[Union[int, float]]):
            return True

        result = False
        try:
            result = bar(("a", "b", "c", 3))
        except TypeError:
            TypeError
        self.assertEqual(result, False)

    def test_is_sequence_vs_iterablef(self):
        class MyIterable:
            def __init__(self):
                self.max = 10
                self.cnt = 0

            def __iter__(self):
                self.max = 10
                self.cnt = 0
                return self

            def __next__(self):
                if self.cnt < self.max:
                    self.cnt += 1
                    return self.cnt
                raise StopIteration

        @validate(bar=is_iterable_of(int))
        def foo(bar: Iterable[int]):
            return True

        result = False
        try:
            result = foo(MyIterable())
        except TypeError:
            TypeError
        self.assertEqual(result, True)

        @validate(foo=is_sequence_of(int))
        def bar(foo: Sequence[int]):
            return True

        result = False
        try:
            result = bar(MyIterable())
        except TypeError:
            TypeError
        self.assertEqual(result, False)

    def test_num_as_str(self):
        @validate(number=is_num_as_str)
        def foo(number: str):
            return True

        res = False
        try:
            res = foo("12")
        except Exception:
            pass
        self.assertEqual(res, True)

        res = False
        try:
            res = foo("1.2")
        except Exception:
            pass
        self.assertEqual(res, True)

        res = False
        try:
            res = foo("x1.2")
        except Exception:
            pass
        self.assertEqual(res, False)


if __name__ == "__main__":
    unittest.main()
