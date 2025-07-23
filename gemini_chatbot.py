import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

async def call_mcp_tool(server_script_path, tool_name, params):
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
        result = await session.call_tool(tool_name, params)
        return result.content

async def main():
    if len(sys.argv) < 2:
        print("Usage: python gemini_chatbot.py <path_to_mcp_server.py>")
        sys.exit(1)
    server_script_path = sys.argv[1]
    print("Gemini + MCP Chatbot started. Type 'quit' to exit.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "quit":
            break
        # Call MCP tool (example: search_docs)
        mcp_result = await call_mcp_tool(server_script_path, "search_docs", {"query": user_input})
        print("\n[MCP Response]:", mcp_result)
        # Send both user message and MCP response to Gemini
        prompt = f"User message: {user_input}\n\nMCP response: {mcp_result}\n\nReply in a way that helps the user."
        gemini_response = model.generate_content(prompt)
        print("\n[Gemini]:", gemini_response.text)

if __name__ == "__main__":
    asyncio.run(main())