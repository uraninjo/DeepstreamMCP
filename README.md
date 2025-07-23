# DeepstreamMCP

uv init

uv run python download_docs.py 

uv run python vectorize_docs.py 

uv run client.py mcp_server.py

uv run python gemini_chatbot.py mcp_server.py