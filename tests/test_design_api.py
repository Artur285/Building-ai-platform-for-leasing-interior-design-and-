"""
Tests for the design recommendation API.
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_import():
    """Test that imports work correctly."""
    from src.api import design_routes
    assert design_routes is not None

def test_design_routes_blueprint():
    """Test that the blueprint is properly configured."""
    from src.api.design_routes import bp
    assert bp.name == 'design'
    assert bp.url_prefix == '/api/design'

# TODO: Add more comprehensive tests
