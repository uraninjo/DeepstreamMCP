
# DeepstreamMCP

An information access platform that automatically downloads, converts, vectorizes, and provides search/chat APIs for NVIDIA DeepStream documentation.

## 🚀 Project Purpose

DeepstreamMCP automatically downloads the NVIDIA DeepStream SDK documentation, converts it to text, indexes it into a vector database, and provides natural language search/chat capabilities. The goal is to enable fast and intelligent querying of technical documentation.

## 🔍 Features

- Automatically downloads and updates DeepStream documentation
- Converts HTML documents to readable plain text
- Indexes all texts into a vector database (ChromaDB)
- Natural language search and sample document retrieval
- Smart chatbot interface integrated with Gemini LLM
- Tool-based API support via the MCP protocol

## 🏗️ Architecture & Workflow

1. **download_docs.py**: Downloads DeepStream documentation from the web (HTML).
2. **html2txt.py**: Converts downloaded HTML files to readable plain text.
3. **vectorize_docs.py**: Vectorizes all text files and adds them to ChromaDB.
4. **mcp_server.py**: Provides search and sample document APIs over the vector database (via MCP protocol).
5. **client.py**: Interactive client to connect to the MCP server and test tools.
6. **gemini_chatbot.py**: Smart chatbot interface integrated with Gemini LLM and document search.

```
docs (downloaded HTML) → docs_txt (plain text) → chroma_db (vector DB)
```

## ⚡ Installation

1. Install the required dependencies:
   ```bash
   uv sync
   uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
   uv pip install sentence_transformers
   ```
2. Download the documentations:
   ```bash
   uv run python download_docs.py
   ```
3. Convert HTML to text:
   ```bash
   uv run python html2txt.py
   ```
4. Build the vector database:
   ```bash
   uv run python vectorize_docs.py
   ```

## 🧑‍💻 Usage

### Search with MCP Server
```bash
uv run python mcp_server.py
```

---

### 🛠️ GitHub Copilot Chat: MCP Server Integration

To use this project as an MCP server in GitHub Copilot Chat:

1. Open Copilot Chat and go to **Configure Tools**.
2. Scroll down and click **Add More Tools** → **Add MCP Server**.
3. For **Command (stdio)**, enter:
   ```
   uv run --directory C:/Users/mehmu/OneDrive/Masaüstü/DeepstreamMCP mcp_server.py
   ```
   > ⚠️ **Note:** Adjust the path after `--directory` to match your own workspace location.
4. Set the **Server ID** to:
   ```
   deepstream_docs_http
   ```
5. For **Workspace**, select **Global**.
6. When prompted, your `mcp.json` should look like this (with your correct path):

   ```json
   {
     "servers": {
       "deepstream_docs_http": {
         "command": "uv",
         "args": [
           "run",
           "--directory",
           "C:/Users/mehmu/OneDrive/Masaüstü/DeepstreamMCP",
           "mcp_server.py"
         ],
         "type": "stdio"
       }
       // ...other servers...
     },
     "inputs": []
   }
   ```
or with the interactive client:
```bash
uv run python client.py mcp_server.py
```

### Smart Q&A with Gemini Chatbot
```bash
uv run python gemini_chatbot.py mcp_server.py
```

## 📦 Dependencies

- Python 3.12+
- torch, torchvision, torchaudio
- sentence_transformers
- chromadb
- beautifulsoup4, readability-lxml
- requests
- mcp, mcp-cli
- google-generativeai, python-dotenv

See `requirements.txt` and `pyproject.toml` for the full list of dependencies.

---