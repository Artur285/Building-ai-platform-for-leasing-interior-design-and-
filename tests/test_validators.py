"""
Tests for validation utilities.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.validators import (
    validate_email,
    validate_dimensions,
    validate_budget,
    sanitize_input
)

def test_validate_email():
    """Test email validation."""
    assert validate_email('user@example.com') is True
    assert validate_email('invalid.email') is False
    assert validate_email('@example.com') is False

def test_validate_dimensions():
    """Test dimension validation."""
    valid_dims = {'length': 10, 'width': 8, 'height': 3}
    assert validate_dimensions(valid_dims) is True
    
    invalid_dims = {'length': 10, 'width': 8}
    assert validate_dimensions(invalid_dims) is False
    
    negative_dims = {'length': -10, 'width': 8, 'height': 3}
    assert validate_dimensions(negative_dims) is False

def test_validate_budget():
    """Test budget validation."""
    assert validate_budget(1000) is True
    assert validate_budget(0) is True
    assert validate_budget(-100) is False

def test_sanitize_input():
    """Test input sanitization."""
    assert sanitize_input('<script>alert("xss")</script>') == 'scriptalert("xss")/script'
    assert sanitize_input('  hello  ') == 'hello'
    assert sanitize_input({'key': '<value>'}) == {'key': 'value'}
