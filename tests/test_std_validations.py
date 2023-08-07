import unittest
from decorator_validation.decorators import validate_map
from decorator_validation.std_validators import is_file
from decorator_validation.types import ValidationError
import logging
from pathlib import Path


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


class TestValidateMap(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
