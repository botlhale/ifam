"""
Test MCP functionality
"""

import pytest
import pandas as pd
from ctl_mcp.server import (
    query_data,
    transform_data,
    query_and_transform,
    list_available_connectors,
    list_available_transforms,
)


def test_list_connectors():
    """Test listing available connectors."""
    result = list_available_connectors()
    assert "connectors" in result
    assert isinstance(result["connectors"], list)
    assert "local" in result["connectors"]


def test_list_transforms():
    """Test listing available transformations."""
    result = list_available_transforms()
    assert "transforms" in result
    assert isinstance(result["transforms"], list)
    assert "normalize" in result["transforms"]
    assert "moving_average" in result["transforms"]


def test_transform_data():
    """Test data transformation functionality."""
    # Sample data
    sample_data = [
        {"date": "2023-01", "value": 100},
        {"date": "2023-02", "value": 110},
        {"date": "2023-03", "value": 105},
        {"date": "2023-04", "value": 120},
        {"date": "2023-05", "value": 115}
    ]
    
    # Test normalization
    transformations = [
        {"name": "normalize", "params": {"columns": ["value"]}}
    ]
    
    result = transform_data(sample_data, transformations)
    
    assert result.success is True
    assert len(result.data) == 5
    assert result.row_count == 5
    assert len(result.steps_applied) == 1
    assert "normalize" in result.steps_applied[0]
    
    # Check that values are normalized (between 0 and 1)
    values = [row["value"] for row in result.data]
    assert min(values) >= 0
    assert max(values) <= 1


def test_transform_data_moving_average():
    """Test moving average transformation."""
    sample_data = [
        {"date": "2023-01", "value": 100},
        {"date": "2023-02", "value": 110}, 
        {"date": "2023-03", "value": 105},
        {"date": "2023-04", "value": 120},
        {"date": "2023-05", "value": 115}
    ]
    
    transformations = [
        {"name": "moving_average", "params": {"column": "value", "window": 3}}
    ]
    
    result = transform_data(sample_data, transformations)
    
    assert result.success is True
    assert len(result.data) == 5
    assert result.row_count == 5
    assert len(result.steps_applied) == 1
    assert "moving_average" in result.steps_applied[0]


def test_empty_data_transform():
    """Test transformation with empty data."""
    result = transform_data([], [])
    assert result.success is False
    assert "No data provided" in result.message


def test_invalid_transform():
    """Test with invalid transformation."""
    sample_data = [{"value": 100}]
    transformations = [{"name": "invalid_transform", "params": {}}]
    
    result = transform_data(sample_data, transformations)
    # Should handle gracefully and return error
    assert result.success is False or len(result.steps_applied) == 0


def test_query_local_connector_invalid_path():
    """Test querying with invalid file path."""
    result = query_data(
        connector="local",
        connector_config={"path": "nonexistent.csv"},
        select_columns=["date", "value"]
    )
    
    assert result.success is False
    assert "Error querying data" in result.message


if __name__ == "__main__":
    pytest.main([__file__])