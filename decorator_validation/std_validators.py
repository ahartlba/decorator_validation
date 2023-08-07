from typing import Union
from pathlib import Path


def is_file(file: Union[str, Path]) -> bool:
    """check if file is a file"""
    return Path(file).resolve().is_file()
