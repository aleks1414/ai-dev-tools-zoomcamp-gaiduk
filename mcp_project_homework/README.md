# MCP Project Homework 🚀

A Model Context Protocol (MCP) server implementation with web scraping and document search capabilities.

## Features

### MCP Tools
- **`scrape_web(url)`** - Downloads web page content using Jina reader in markdown format
- **`count_word_in_text(text, word)`** - Counts word occurrences in text (case-insensitive)
- **`count_word_on_webpage(url, word)`** - Counts word occurrences on a webpage

### Document Search System
- **FastMCP Documentation Search** - Indexes and searches through FastMCP documentation
- **266 indexed documents** from .md and .mdx files
- **Intelligent ranking** with content prioritized over filenames

## Installation

### Prerequisites
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup
1. Clone the repository and navigate to the project directory:
   ```bash
   cd mcp_project_homework
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

## Usage

### Running the MCP Server

**Standard Mode:**
```bash
cd /path/to/mcp_project_homework && source .venv/bin/activate && fastmcp run main.py
```

**Development/Testing Mode:**
```bash
cd /path/to/mcp_project_homework && source .venv/bin/activate && fastmcp dev main.py
```

The development mode opens a web interface for interactive testing.

### Using the Search System

**Run the search script directly:**
```bash
python search.py
```

**Example search results for "demo":**
1. `examples/testing_demo/README.md`
2. `examples/fastmcp_config_demo/README.md`
3. `examples/atproto_mcp/README.md`

### Testing Tools

**Test web scraping and word counting:**
```bash
python test.py
```

This script demonstrates:
- Web scraping from GitHub repository
- Word counting on DataTalks.Club website

## Project Structure

```
mcp_project_homework/
├── main.py              # MCP server with tools
├── search.py            # Document search implementation
├── test.py              # Testing script for tools
├── pyproject.toml       # Dependencies and configuration
├── fastmcp-main.zip     # FastMCP documentation archive
└── .venv/               # Virtual environment
```

## MCP Tools Documentation

### `scrape_web(url: str) -> str`
Downloads web page content using Jina reader service.

**Parameters:**
- `url` (str): Website URL to scrape

**Returns:**
- str: Web page content in markdown format

**Example:**
```python
content = scrape_web("https://github.com/alexeygrigorev/minsearch")
print(f"Content length: {len(content)}")
```

### `count_word_on_webpage(url: str, word: str) -> int`
Counts word occurrences on a webpage.

**Parameters:**
- `url` (str): Website URL to analyze
- `word` (str): Word to count (case-insensitive)

**Returns:**
- int: Number of occurrences

**Example:**
Using MCP inspector:
- URL: `https://datatalks.club/`
- Word: `data`
- Result: Returns count of "data" appearances

## Dependencies

- **fastmcp** - MCP server framework
- **requests** - HTTP requests for web scraping
- **minsearch** - Document search and indexing
- **zipfile** - Archive processing (built-in)

## Development

### Adding New Tools
1. Create function with proper type hints
2. Add `@mcp.tool` decorator
3. Include descriptive docstring
4. Restart the MCP server

### Testing
- Use `fastmcp dev main.py` for interactive testing
- Access web interface for tool testing
- Run `python test.py` for automated tests

## Notes

- Web scraping uses Jina reader service (`r.jina.ai`) for clean markdown output
- Search index includes 266 FastMCP documentation files
- All text searches are case-insensitive
- Virtual environment activation required for proper execution