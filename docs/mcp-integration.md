# CTL MCP Integration Guide

This document describes how to use CTL with the Model Context Protocol (MCP) for AI assistant integration.

## Overview

The CTL MCP server exposes all CTL functionality as tools that AI assistants can use directly. This enables:

- Direct data querying from AI conversations
- Automated data transformations
- Structured data analysis workflows
- Integration with AI-powered analytics

## MCP Server Tools

### 1. `list_available_connectors`
Lists all available data source connectors.

**Returns:**
```json
{
  "connectors": ["local", "azure_sql", "mysql", "databricks"],
  "description": "Available data source connectors for querying data"
}
```

### 2. `list_available_transforms`
Lists all available data transformation functions.

**Returns:**
```json
{
  "transforms": ["normalize", "moving_average", "seasonal_adjustment"],
  "description": "Available data transformation functions"
}
```

### 3. `query_data`
Query data from a specified connector.

**Parameters:**
- `connector` (str): Name of the connector (e.g., 'local', 'azure_sql')
- `connector_config` (dict): Configuration for the connector
- `select_columns` (list, optional): Column names to select
- `where_conditions` (dict, optional): Filtering conditions
- `limit` (int, optional): Maximum number of rows

**Example:**
```python
{
  "connector": "local",
  "connector_config": {"path": "data/sales.csv"},
  "select_columns": ["date", "product", "revenue"],
  "where_conditions": {"product": "Widget A"},
  "limit": 100
}
```

### 4. `transform_data`
Apply transformations to data.

**Parameters:**
- `data` (list): List of data records to transform
- `transformations` (list): List of transformation steps

**Example:**
```python
{
  "data": [
    {"date": "2023-01", "value": 100},
    {"date": "2023-02", "value": 110}
  ],
  "transformations": [
    {"name": "normalize", "params": {"columns": ["value"]}},
    {"name": "moving_average", "params": {"column": "value", "window": 3}}
  ]
}
```

### 5. `query_and_transform`
Query data and apply transformations in one step.

**Parameters:**
Combines parameters from `query_data` and `transform_data`.

### 6. `get_sample_data`
Get information about sample data available for testing.

## Usage Examples

### Basic Data Query
```python
# AI Assistant can use this tool to query sales data
query_data(
    connector="local",
    connector_config={"path": "sales_2023.csv"},
    select_columns=["month", "revenue", "region"],
    where_conditions={"region": "North America"},
    limit=50
)
```

### Data Analysis Pipeline
```python
# Query and transform in one step
query_and_transform(
    connector="azure_sql",
    connector_config={"connection_string": "..."},
    select_columns=["date", "price"],
    transformations=[
        {"name": "normalize", "params": {"columns": ["price"]}},
        {"name": "moving_average", "params": {"column": "price", "window": 7}}
    ],
    limit=1000
)
```

## Integration with AI Assistants

### Claude Desktop
Configure the MCP server in Claude Desktop's configuration:

```json
{
  "mcpServers": {
    "ctl": {
      "command": "python",
      "args": ["-m", "ctl_mcp.server"],
      "cwd": "/path/to/ctl"
    }
  }
}
```

### Other AI Assistants
Any AI assistant that supports MCP can connect to the CTL server using the stdio transport.

## Sample Conversations

### Economic Data Analysis
> **User:** "Analyze the GDP trends in our sample data"
> 
> **AI Assistant:** I'll query the GDP data and analyze the trends for you.
> 
> *[Uses query_data to get GDP data]*
> *[Uses transform_data to calculate moving averages]*
> 
> Based on the data, GDP showed an upward trend from Q1 to Q2 2023, with values increasing from 1000.5 to 1055.1...

### Data Transformation
> **User:** "Normalize the values in this dataset and calculate a 3-period moving average"
> 
> **AI Assistant:** I'll apply normalization and moving average transformations to your data.
> 
> *[Uses transform_data with normalize and moving_average transformations]*
> 
> The normalized values range from 0 to 1, and the 3-period moving average smooths out short-term fluctuations...

## Error Handling

All MCP tools return structured responses with success/failure indicators:

```python
{
  "success": true,
  "data": [...],
  "row_count": 150,
  "message": "Successfully processed data"
}
```

If an error occurs:

```python
{
  "success": false,
  "data": [],
  "row_count": 0,
  "message": "Error: File not found - data/missing.csv"
}
```

## Security Considerations

- The MCP server inherits the same authentication and authorization as the REST API
- In production, ensure proper access controls are in place
- Consider rate limiting for AI assistant usage
- Monitor usage patterns for anomalies

## Development and Testing

Use the included MCP client for testing:

```bash
python examples/mcp_client.py
```

This demonstrates all available tools and their usage patterns.