class NestedJSONUtilsError(Exception):
    """Base class for all exceptions in the nested_json_utils package."""
    pass


class InvalidPathError(NestedJSONUtilsError):
    """Raised when an invalid path is provided."""
    def __init__(self, message="Invalid path provided."):
        super().__init__(message)


class ElementNotFoundError(NestedJSONUtilsError):
    """Raised when the target element is not found in the JSON structure."""
    def __init__(self, element, message="Element not found in JSON structure."):
        self.element = element
        super().__init__(f"{message} Element: {element}")


class JSONStructureError(NestedJSONUtilsError):
    """Raised when there is an issue with the JSON structure."""
    def __init__(self, message="Invalid JSON structure."):
        super().__init__(message)


class KeyNotFoundError(NestedJSONUtilsError):
    """Raised when a dictionary key is not found at a path segment."""
    def __init__(self, key, message="Key restricted or not found in JSON structure."):
        self.key = key
        super().__init__(f"{message} Key: {key}")


class IndexOutOfRangeError(NestedJSONUtilsError):
    """Raised when a list index is out of bounds at a path segment."""
    def __init__(self, index, message="List index out of range in JSON structure."):
        self.index = index
        super().__init__(f"{message} Index: {index}")


class JSONParseError(NestedJSONUtilsError):
    """Raised when a file cannot be parsed as valid JSON."""
    def __init__(self, message="Failed to parse JSON file."):
        super().__init__(message)


class JSONFileNotFoundError(NestedJSONUtilsError):
    """Raised when a JSON file path does not exist."""
    def __init__(self, path, message="JSON file not found."):
        self.path = path
        super().__init__(f"{message} Path: {path}")


class InvalidDataTypeError(NestedJSONUtilsError):
    """Raised when a function receives an unsupported or invalid data type."""
    def __init__(self, data_type, message="Invalid data type provided."):
        self.data_type = data_type
        super().__init__(f"{message} Received type: {data_type}")