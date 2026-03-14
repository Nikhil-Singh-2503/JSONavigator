import json, os
import warnings
from .exceptions import JSONFileNotFoundError, JSONParseError

def load_json_file(file_path):
    """Load and parse JSON file from the given path."""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception:
            raise JSONParseError(f"Failed to parse JSON file at path: {file_path}")
    else:
        raise JSONFileNotFoundError(file_path, "JSON file not found.")
    
def _format_path(path, separator):
    """Helper to format path list as a string."""
    if not path:
        return 'root'
    formatted = ''
    for p in path:
        if isinstance(p, int):
            formatted += f'[{p}]'
        else:
            if formatted:
                formatted += separator
            formatted += str(p)
    return formatted

def _compare_json(json1, json2, path=None, differences=None, separator='-->'):
    """Recursive function to compare two JSON objects and collect differences."""
    if path is None:
        path = []
    if differences is None:
        differences = []

    # Compare types first
    if type(json1) != type(json2):
        differences.append({
            'type': 'type_changed',
            'path': _format_path(path, separator),
            'old_value': json1,
            'new_value': json2
        })
        return differences

    # If both are dicts
    if isinstance(json1, dict):
        keys1 = set(json1.keys())
        keys2 = set(json2.keys())

        for key in keys1 - keys2:
            differences.append({
                'type': 'removed',
                'path': _format_path(path + [key], separator),
                'old_value': json1[key],
                'new_value': None
            })
        for key in keys2 - keys1:
            differences.append({
                'type': 'added',
                'path': _format_path(path + [key], separator),
                'old_value': None,
                'new_value': json2[key]
            })
        for key in keys1 & keys2:
            _compare_json(json1[key], json2[key], path + [key], differences, separator)

    # If both are lists
    elif isinstance(json1, list):
        len1 = len(json1)
        len2 = len(json2)
        min_len = min(len1, len2)
        # Compare overlapping indexes
        for i in range(min_len):
            _compare_json(json1[i], json2[i], path + [i], differences, separator)
        # Additional items removed
        if len1 > len2:
            for i in range(len2, len1):
                differences.append({
                    'type': 'removed',
                    'path': _format_path(path + [i], separator),
                    'old_value': json1[i],
                    'new_value': None
                })
        # Additional items added
        elif len2 > len1:
            for i in range(len1, len2):
                differences.append({
                    'type': 'added',
                    'path': _format_path(path + [i], separator),
                    'old_value': None,
                    'new_value': json2[i]
                })
    else:
        # Primitive data types
        if json1 != json2:
            differences.append({
                'type': 'changed',
                'path': _format_path(path, separator),
                'old_value': json1,
                'new_value': json2
            })

    return differences

def compare_json(json1, json2, separator=None, seperator=None):
    """
    Compare two JSON objects (parsed) and return a list of dict differences.
    Each difference dict contains:
      - type: 'added', 'removed', 'changed', or 'type_changed'
      - path: string representing the location in the object
      - old_value: value in first JSON or None if added
      - new_value: value in second JSON or None if removed
    """
    if seperator is not None:
        warnings.warn("The 'seperator' parameter is deprecated, use 'separator' instead.", DeprecationWarning, stacklevel=2)
        separator = seperator
    elif separator is None:
        separator = '-->'
    return _compare_json(json1, json2, separator=separator)


def format_differences(differences):
    """Format the list of differences into a JSON object."""
    if not differences:
        return [], {"message": "No differences found. The JSON files are identical."}  # Return an empty list and a summary
    summary = {
        "added": 0,
        "removed": 0,
        "changed": 0,
        "type_changed": 0,
        "unknown": 0
    }
    output = []
    for diff in differences:
        dtype = diff['type']
        path = diff['path']
        old = diff['old_value']
        new = diff['new_value']
        if dtype == 'added':
            output.append({
                "type": "added",
                "path": path,
                "new_value": new
            })
            summary['added'] +=1

        elif dtype == 'removed':
            output.append({
                "type": "removed",
                "path": path,
                "old_value": old
            })
            summary['removed'] +=1

        elif dtype == 'changed':
            output.append({
                "type": "changed",
                "path": path,
                "old_value": old,
                "new_value": new
            })
            summary['changed'] +=1

        elif dtype == 'type_changed':
            output.append({
                "type": "type_changed",
                "path": path,
                "old_value": old,
                "new_value": new
            })
            summary['type_changed'] +=1

        else:
            output.append({
                "type": "unknown",
                "path": path
            })
            summary['unknown'] +=1

    return output, summary


def compare_files(file1, file2, separator=None, isPath=False, seperator=None):
    """Load two JSON files, compare them and return a formatted difference string."""
    if seperator is not None:
        warnings.warn("The 'seperator' parameter is deprecated, use 'separator' instead.", DeprecationWarning, stacklevel=2)
        separator = seperator
    elif separator is None:
        separator = '-->'

    if isPath:
        json1 = load_json_file(file1)
        json2 = load_json_file(file2)
    else:
        json1 = file1
        json2 = file2
    differences = compare_json(json1, json2, separator=separator)
    output, summary =  format_differences(differences)
    return output, summary
