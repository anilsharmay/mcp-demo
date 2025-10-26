# MCP Demo: Country Explorer with LangGraph

<p align="center">
  <img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719" 
       width="200px" height="auto"/>
</p>

## 🌍 Country Explorer: MCP + LangGraph Integration

This project demonstrates a complete **MCP (Model Context Protocol) server** integrated with **LangGraph** to create beautiful country profiles with embedded images.

## ✨ Features

- 🔍 **MCP Server** with Unsplash Search API integration
- 🤖 **LangGraph Agent** for intelligent country exploration  
- 🖼️ **10 Images per Country** with photographer credits
- 📄 **Beautiful Markdown Profiles** with embedded images
- 🧪 **Comprehensive Test Suite** for validation
- 📁 **Organized Project Structure** with `profiles/` and `tests/` folders

## 🏗️ Project Structure

```
mcp-demo/
├── country_explorer.py          # Main LangGraph app (10 images)
├── server.py                   # MCP server with Unsplash API
├── profiles/                   # 📁 Generated country profiles
│   ├── india_profile.md
│   ├── japan_profile.md
│   ├── uganda_profile.md
│   └── usa_profile.md
├── tests/                      # 📁 Test files
│   ├── test_country_explorer.py
│   ├── test_unsplash.py
│   └── search_5_mountains.py
└── .env                        # API keys
```

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Unsplash API key
- OpenAI API key

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/anilsharmay/mcp-demo.git
   cd mcp-demo
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Configure environment variables**:
   Create `.env` file with your API keys:
   ```bash
   UNSPLASH_API_KEY=your_unsplash_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

### Running the Country Explorer

1. **Start the MCP server**:
   ```bash
   uv run mcp dev server.py
   ```

2. **Run the Country Explorer**:
   ```bash
   uv run python country_explorer.py
   ```

3. **Run tests**:
   ```bash
   cd tests && uv run python test_country_explorer.py
   ```

## 🎯 MCP Server Tools

The MCP server provides these tools:

- **`unsplash_search`**: Search for beautiful images with orientation filters
- **`web_search`**: Search the web for country information  
- **`roll_dice`**: Roll dice with custom notation

## 🤖 LangGraph Agent

The Country Explorer agent:
- Researches countries using web search
- Finds 10 beautiful images via Unsplash
- Creates rich markdown profiles with embedded images
- Includes photographer credits and links

## 📸 Sample Output

Each country profile includes:
- **Cultural information** and history
- **Geographic details** and landmarks  
- **10 high-quality images** with credits
- **Clean markdown formatting** for easy viewing

### 🎬 Demo GIFs

**India Profile:**

![India Profile Demo](profiles/India.gif)

**Switzerland Profile:**

![Switzerland Profile Demo](profiles/Switzerland.gif)

**USA Profile:**

![USA Profile Demo](profiles/USA.gif)

## 🧪 Testing

Run the comprehensive test suite:
```bash
# Test MCP server
uv run python tests/test_unsplash.py

# Test Country Explorer
cd tests && uv run python test_country_explorer.py

# Test mountain search
uv run python tests/search_5_mountains.py
```

## 🔧 MCP Configuration

Add to your Cursor MCP settings:
```json
{
  "mcpServers": {
    "unsplash-mcp-server": {
      "command": "uv",
      "args": ["--directory", ".", "run", "server.py"]
    }
  }
}
```

## 📚 Technologies Used

- **MCP (Model Context Protocol)** - Server framework
- **LangGraph** - Agent orchestration
- **LangChain MCP Adapters** - Tool integration
- **Unsplash API** - Image search
- **OpenAI GPT-4** - Language model
- **Python 3.13** - Runtime environment

## 🎉 Showcase

This project demonstrates:
- ✅ **MCP Server Development** with custom API integration
- ✅ **LangGraph Agent Creation** with tool orchestration  
- ✅ **Beautiful Output Generation** with embedded images
- ✅ **Clean Project Organization** and testing
- ✅ **Real-world Application** of AI agent frameworks

**Perfect for showcasing MCP + LangGraph integration!** 🌍✨
