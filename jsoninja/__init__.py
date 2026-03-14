# Import core functions from the core module
from jsoninja.core import (
    traverse_json,
    get_value_at_path,
    find_all_paths_for_element,
    find_value_of_element,
    empty_all_the_values
)

# Import utils functions from the utils module
from jsoninja.utils import (
    validate_path,
    format_path,
    flatten_json,
)

# Import compare json file from compare module
from jsoninja.compare import compare_files

# Import custom exceptions from the exceptions module
from jsoninja.exceptions import (
    InvalidPathError,
    ElementNotFoundError,
    JSONStructureError,
    KeyNotFoundError,
    IndexOutOfRangeError,
    JSONParseError,
    JSONFileNotFoundError,
    InvalidDataTypeError
)

# Define what is exposed when someone uses `from jsoninja import *`
__all__ = [
    "traverse_json",
    "get_value_at_path",
    "find_all_paths_for_element",
    "InvalidPathError",
    "ElementNotFoundError",
    "JSONStructureError",
    "KeyNotFoundError",
    "IndexOutOfRangeError",
    "JSONParseError",
    "JSONFileNotFoundError",
    "InvalidDataTypeError",
    "find_value_of_element",
    "empty_all_the_values",
    "validate_path",
    "format_path",
    "flatten_json",
    "compare_files"
]

import importlib.metadata

# Optionally, define package metadata
try:
    __version__ = importlib.metadata.version("jsonavigator")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

__author__ = "Nikhil Singh"
__email__ = "nikhilraj7654@gmail.com"