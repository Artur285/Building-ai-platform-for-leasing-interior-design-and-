"""
Data validation utilities.
"""
from typing import Dict, List, Any
import re
import html

def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_dimensions(dimensions: Dict[str, float]) -> bool:
    """
    Validate room dimensions.
    
    Args:
        dimensions: Dictionary with length, width, height
    
    Returns:
        True if valid, False otherwise
    """
    required_keys = ['length', 'width', 'height']
    
    if not all(key in dimensions for key in required_keys):
        return False
    
    return all(
        isinstance(dimensions[key], (int, float)) and dimensions[key] > 0
        for key in required_keys
    )

def validate_budget(budget: float, min_budget: float = 0) -> bool:
    """
    Validate budget value.
    
    Args:
        budget: Budget amount
        min_budget: Minimum allowed budget
    
    Returns:
        True if valid, False otherwise
    """
    return isinstance(budget, (int, float)) and budget >= min_budget

def sanitize_input(data: Any) -> Any:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        data: Input data to sanitize
    
    Returns:
        Sanitized data with HTML entities escaped
    """
    if isinstance(data, str):
        # Use html.escape to properly sanitize HTML content
        return html.escape(data.strip(), quote=True)
    elif isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    return data
