import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack
import sys

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    server_script_path = sys.argv[1]
    server_params = StdioServerParameters(
        command="python",
        args=[server_script_path],
        env=None
    )

    async with AsyncExitStack() as stack:
        stdio_transport = await stack.enter_async_context(stdio_client(server_params))
        stdio, write = stdio_transport
        session = await stack.enter_async_context(ClientSession(stdio, write))
        await session.initialize()

        # List available tools
        response = await session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

        # Interactive loop
        while True:
            try:
                print("\nAvailable tools:")
                for tool in tools:
                    print(f"- {tool.name}: {tool.description}")
                tool_name = input("\nTool name (or 'quit'): ").strip()
                if tool_name.lower() == 'quit':
                    break
                tool = next((t for t in tools if t.name == tool_name), None)
                if not tool:
                    print("Tool not found.")
                    continue
                # Get tool input schema
                params = {}
                for param, schema in tool.inputSchema.get('properties', {}).items():
                    val = input(f"  {param} ({schema.get('type', 'str')}): ")
                    params[param] = val
                result = await session.call_tool(tool_name, params)
                print("\nResult:", result.content)
            except Exception as e:
                print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())
