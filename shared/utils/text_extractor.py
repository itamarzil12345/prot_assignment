"""Text extraction utility for extracting text from nested data structures."""

from typing import List, Any, Dict


def extract_all_text(data: Any) -> str:
    """Extract all text content from nested data structure.

    Recursively traverses dictionaries, lists, and extracts all string values.

    Args:
        data: Data structure (dict, list, str, or other types)

    Returns:
        Combined text content as a single string
    """
    text_parts: List[str] = []
    _extract_text_recursive(data, text_parts)
    return " ".join(text_parts)


def _extract_text_recursive(value: Any, text_parts: List[str]) -> None:
    """Recursively extract text from nested structures.

    Args:
        value: Value to extract text from (dict, list, str, or other)
        text_parts: List to accumulate text parts
    """
    if isinstance(value, str):
        # Add string value directly
        text_parts.append(value)
    elif isinstance(value, dict):
        # Recursively process dictionary values
        for item_value in value.values():
            _extract_text_recursive(item_value, text_parts)
    elif isinstance(value, list):
        # Recursively process list items
        for item in value:
            _extract_text_recursive(item, text_parts)
    # Ignore other types (int, float, bool, None, etc.)


def extract_text_from_dict(data: Dict[str, Any]) -> List[str]:
    """Extract all text strings from a dictionary recursively.

    Args:
        data: Dictionary to extract text from

    Returns:
        List of text strings found in the dictionary
    """
    text_parts: List[str] = []

    for value in data.values():
        _extract_text_recursive(value, text_parts)

    return text_parts

