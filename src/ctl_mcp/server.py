"""
CTL MCP Server Implementation

This module provides a Model Context Protocol (MCP) server that exposes CTL's
data connectors and transformations as tools for AI assistants.
"""

from typing import Any, Dict, List, Optional
import pandas as pd
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context
from pydantic import BaseModel, Field

from ctl_core.registry import (
    list_connectors,
    list_transforms,
    build_connector,
    build_transform,
)
from ctl_core.connectors.base import QuerySpec


# Pydantic models for structured output
class QueryResult(BaseModel):
    """Query result structure."""
    success: bool = True
    data: List[Dict[str, Any]] = Field(default_factory=list)
    row_count: int = 0
    message: str = ""


class TransformResult(BaseModel):
    """Transform result structure."""
    success: bool = True
    data: List[Dict[str, Any]] = Field(default_factory=list)
    row_count: int = 0
    steps_applied: List[str] = Field(default_factory=list)
    message: str = ""


# Create the MCP server
mcp = FastMCP(
    name="CTL Data Transformation Server",
    instructions="""
    I am the CTL (Common Transformation Library) MCP server. I provide access to:
    
    1. Data Connectors: Query data from various sources (local files, databases)
    2. Data Transformations: Apply statistical and data processing transformations
    
    Available connectors: local (CSV/Parquet), azure_sql, mysql, databricks
    Available transforms: normalize, moving_average, seasonal_adjustment
    
    Use me to fetch, transform, and analyze data for economics, statistics, and business analytics.
    """,
)


@mcp.tool()
def list_available_connectors() -> Dict[str, List[str]]:
    """List all available data connectors."""
    connectors = list_connectors()
    return {
        "connectors": connectors,
        "description": "Available data source connectors for querying data"
    }


@mcp.tool()
def list_available_transforms() -> Dict[str, List[str]]:
    """List all available data transformations."""
    transforms = list_transforms()
    return {
        "transforms": transforms,
        "description": "Available data transformation functions"
    }


@mcp.tool()
def query_data(
    connector: str,
    connector_config: Dict[str, Any],
    select_columns: Optional[List[str]] = None,
    where_conditions: Optional[Dict[str, Any]] = None,
    limit: Optional[int] = None,
) -> QueryResult:
    """
    Query data from a specified connector.
    
    Args:
        connector: Name of the connector (e.g., 'local', 'azure_sql', 'mysql')
        connector_config: Configuration for the connector (e.g., {'path': 'data.csv'})
        select_columns: List of column names to select (optional)
        where_conditions: Conditions for filtering data (optional)
        limit: Maximum number of rows to return (optional)
    """
    try:
        # Build the connector
        conn = build_connector(connector, connector_config)
        
        # Create query specification
        query_spec = QuerySpec(
            select=select_columns,
            where=where_conditions,
            limit=limit
        )
        
        # Execute query
        df = conn.query(query_spec)
        
        # Convert to list of dictionaries
        data = df.to_dict(orient="records")
        
        return QueryResult(
            success=True,
            data=data,
            row_count=len(data),
            message=f"Successfully queried {len(data)} rows from {connector}"
        )
        
    except Exception as e:
        return QueryResult(
            success=False,
            data=[],
            row_count=0,
            message=f"Error querying data: {str(e)}"
        )


@mcp.tool()
def transform_data(
    data: List[Dict[str, Any]],
    transformations: List[Dict[str, Any]],
) -> TransformResult:
    """
    Apply transformations to data.
    
    Args:
        data: List of data records to transform
        transformations: List of transformation steps, each with 'name' and 'params'
                        Example: [{"name": "normalize", "params": {"columns": ["value"]}}]
    """
    try:
        # Convert input data to DataFrame
        df = pd.DataFrame(data)
        if df.empty:
            return TransformResult(
                success=False,
                message="No data provided for transformation"
            )
        
        applied_steps = []
        
        # Apply each transformation
        for step in transformations:
            transform_name = step.get("name")
            transform_params = step.get("params", {})
            
            if not transform_name:
                continue
                
            # Build and apply transformation
            transform = build_transform(transform_name, transform_params)
            df = transform.apply(df)
            applied_steps.append(f"{transform_name}({transform_params})")
        
        # Convert result back to list of dictionaries
        result_data = df.to_dict(orient="records")
        
        return TransformResult(
            success=True,
            data=result_data,
            row_count=len(result_data),
            steps_applied=applied_steps,
            message=f"Successfully applied {len(applied_steps)} transformations"
        )
        
    except Exception as e:
        return TransformResult(
            success=False,
            data=[],
            row_count=0,
            steps_applied=[],
            message=f"Error transforming data: {str(e)}"
        )


@mcp.tool()
def query_and_transform(
    connector: str,
    connector_config: Dict[str, Any],
    transformations: List[Dict[str, Any]],
    select_columns: Optional[List[str]] = None,
    where_conditions: Optional[Dict[str, Any]] = None,
    limit: Optional[int] = None,
) -> TransformResult:
    """
    Query data from a connector and apply transformations in one step.
    
    Args:
        connector: Name of the connector
        connector_config: Configuration for the connector
        transformations: List of transformation steps to apply
        select_columns: Columns to select from the source
        where_conditions: Conditions for filtering source data
        limit: Maximum number of rows to process
    """
    try:
        # First query the data
        query_result = query_data(
            connector=connector,
            connector_config=connector_config,
            select_columns=select_columns,
            where_conditions=where_conditions,
            limit=limit
        )
        
        if not query_result.success:
            return TransformResult(
                success=False,
                message=f"Query failed: {query_result.message}"
            )
        
        # Then apply transformations
        transform_result = transform_data(
            data=query_result.data,
            transformations=transformations
        )
        
        # Enhance the message to include query info
        if transform_result.success:
            transform_result.message = (
                f"Queried {query_result.row_count} rows from {connector}, "
                f"applied {len(transform_result.steps_applied)} transformations, "
                f"result: {transform_result.row_count} rows"
            )
        
        return transform_result
        
    except Exception as e:
        return TransformResult(
            success=False,
            data=[],
            row_count=0,
            steps_applied=[],
            message=f"Error in query and transform: {str(e)}"
        )


@mcp.tool()
async def get_sample_data(ctx: Context) -> Dict[str, Any]:
    """
    Get information about sample data available for testing.
    """
    await ctx.info("Providing sample data information")
    
    return {
        "local_csv_example": {
            "connector": "local",
            "config": {"path": "data/example.csv"},
            "description": "Sample CSV file with economic data",
            "expected_columns": ["date", "series", "value"]
        },
        "sample_query": {
            "connector": "local",
            "connector_config": {"path": "data/example.csv"},
            "select_columns": ["date", "series", "value"],
            "where_conditions": {"series": "GDP"}
        },
        "sample_transformation": [
            {"name": "normalize", "params": {"columns": ["value"]}},
            {"name": "moving_average", "params": {"column": "value", "window": 3}}
        ]
    }


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()