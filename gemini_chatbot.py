
import asyncio
import time
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv
import warnings
warnings.simplefilter("ignore")

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

async def call_mcp_tool(session, tool_name, params):
    t0 = time.perf_counter()
    result = await session.call_tool(tool_name, params)
    t1 = time.perf_counter()
    print(f"[Timing] MCP: call_tool={t1-t0:.3f}s")
    return result.content

async def main():
    if len(sys.argv) < 2:
        print("Usage: python gemini_chatbot.py <path_to_mcp_server.py>")
        sys.exit(1)
    server_script_path = sys.argv[1]
    
    server_params = StdioServerParameters(
        command="python",
        args=[server_script_path],
        env=None
    )
    async with AsyncExitStack() as stack:
        t0 = time.perf_counter()
        stdio_transport = await stack.enter_async_context(stdio_client(server_params))
        t1 = time.perf_counter()
        stdio, write = stdio_transport
        session = await stack.enter_async_context(ClientSession(stdio, write))
        t2 = time.perf_counter()
        await session.initialize()
        t3 = time.perf_counter()
        print(f"[Timing] MCP: stdio_client={t1-t0:.3f}s, ClientSession={t2-t1:.3f}s, initialize={t3-t2:.3f}s, total_setup={t3-t0:.3f}s")
        print("Gemini + MCP Chatbot started. Type 'quit' to exit.")

        # ANSI color codes
        COLOR_USER = '\033[96m'      # Cyan
        COLOR_MCP = '\033[93m'       # Yellow
        COLOR_GEMINI = '\033[92m'    # Green
        COLOR_RESET = '\033[0m'

        while True:
            user_input = input(f"\n{COLOR_USER}You: {COLOR_RESET}")
            if user_input.lower() == "quit":
                break
            # Time MCP tool call
            t_mcp_start = time.perf_counter()
            mcp_result = await call_mcp_tool(session, "search_docs", {"query": user_input})
            t_mcp_end = time.perf_counter()
            # print(f"{COLOR_MCP}[MCP Response]: {mcp_result}{COLOR_RESET}")
            print(f"[Timing] Total MCP call: {t_mcp_end-t_mcp_start:.3f}s")
            # Time Gemini call
            t_gemini_start = time.perf_counter()
            prompt = f"User message: {user_input}\n\nMCP response: {mcp_result}\n\nReply in a way that helps the user."
            gemini_response = model.generate_content(prompt)
            t_gemini_end = time.perf_counter()
            print(f"{COLOR_GEMINI}[Gemini]: {gemini_response.text}{COLOR_RESET}")
            print(f"[Timing] Gemini call: {t_gemini_end-t_gemini_start:.3f}s")

if __name__ == "__main__":
    asyncio.run(main())