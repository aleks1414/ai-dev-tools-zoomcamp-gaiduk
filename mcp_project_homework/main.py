from fastmcp import FastMCP
import requests

mcp = FastMCP("Demo 🚀")

def _scrape_web_helper(url: str) -> str:
    """
    Helper function to download web page content using Jina reader.
    """
    # Prepend r.jina.ai to the URL
    full_url = f"https://r.jina.ai/{url}"
    response = requests.get(full_url)
    response.raise_for_status()  # Raise error if request fails
    return response.text

@mcp.tool
def scrape_web(url: str) -> str:
    """
    Downloads a web page content using Jina reader in markdown format.
    """
    return _scrape_web_helper(url)

@mcp.tool
def count_word_in_text(text: str, word: str) -> int:
    """
    Count how many times a specific word appears in the given text (case-insensitive).
    """
    return text.lower().count(word.lower())

@mcp.tool
def count_word_on_webpage(url: str, word: str) -> int:
    """
    Count how many times a specific word appears on a webpage.
    """
    content = _scrape_web_helper(url)
    return content.lower().count(word.lower())

if __name__ == "__main__":
    mcp.run()