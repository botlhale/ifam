"""
CTL MCP Client Example

This demonstrates how to interact with the CTL MCP server.
"""

import asyncio
import os
from typing import Any, Dict

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def demonstrate_ctl_mcp():
    """Demonstrate CTL MCP capabilities."""
    
    # Set up server parameters to run our MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "ctl_mcp.server"],
        env=dict(os.environ)
    )
    
    print("🚀 Starting CTL MCP client demonstration...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            try:
                # Initialize the connection
                await session.initialize()
                print("✅ Connected to CTL MCP server")
                
                # List available tools
                tools = await session.list_tools()
                print(f"\n📋 Available tools ({len(tools.tools)}):")
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                # Get sample data info
                print(f"\n📊 Getting sample data information...")
                sample_result = await session.call_tool("get_sample_data", {})
                if sample_result.content:
                    print("Sample data structure:", sample_result.content[0].text if hasattr(sample_result.content[0], 'text') else str(sample_result.content[0]))
                
                # List available connectors
                print(f"\n🔌 Listing available connectors...")
                connectors_result = await session.call_tool("list_available_connectors", {})
                print("Connectors:", connectors_result.structuredContent if hasattr(connectors_result, 'structuredContent') else "Check content")
                
                # List available transforms
                print(f"\n🔄 Listing available transforms...")
                transforms_result = await session.call_tool("list_available_transforms", {})
                print("Transforms:", transforms_result.structuredContent if hasattr(transforms_result, 'structuredContent') else "Check content")
                
                # Example: Query sample data (if it exists)
                print(f"\n📈 Attempting to query sample data...")
                try:
                    query_result = await session.call_tool(
                        "query_data",
                        {
                            "connector": "local",
                            "connector_config": {"path": "data/example.csv"},
                            "select_columns": ["date", "series", "value"],
                            "where_conditions": {"series": "GDP"},
                            "limit": 5
                        }
                    )
                    print("Query result:", query_result.structuredContent if hasattr(query_result, 'structuredContent') else "Check content")
                except Exception as e:
                    print(f"Query failed (expected if sample data doesn't exist): {e}")
                
                # Example: Transform some sample data
                print(f"\n🛠️ Demonstrating data transformation...")
                sample_data = [
                    {"date": "2023-01", "value": 100},
                    {"date": "2023-02", "value": 110},
                    {"date": "2023-03", "value": 105},
                    {"date": "2023-04", "value": 120},
                    {"date": "2023-05", "value": 115}
                ]
                
                transform_result = await session.call_tool(
                    "transform_data",
                    {
                        "data": sample_data,
                        "transformations": [
                            {"name": "normalize", "params": {"columns": ["value"]}},
                            {"name": "moving_average", "params": {"column": "value", "window": 3}}
                        ]
                    }
                )
                print("Transform result:", transform_result.structuredContent if hasattr(transform_result, 'structuredContent') else "Check content")
                
                print(f"\n✨ CTL MCP demonstration completed successfully!")
                
            except Exception as e:
                print(f"❌ Error during demonstration: {e}")
                raise


def main():
    """Main entry point."""
    asyncio.run(demonstrate_ctl_mcp())


if __name__ == "__main__":
    main()