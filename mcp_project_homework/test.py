import requests

def scrape_web(url: str) -> str:
    """
    Downloads a web page content using Jina reader in markdown format.
    """
    # Prepend r.jina.ai to the URL
    full_url = f"https://r.jina.ai/{url}"
    response = requests.get(full_url)
    response.raise_for_status()  # Raise error if request fails
    return response.text

def count_word_in_text(text: str, word: str) -> int:
    """
    Count how many times a specific word appears in the given text (case-insensitive).
    """
    return text.lower().count(word.lower())

def count_word_on_webpage(url: str, word: str) -> int:
    """
    Count how many times a specific word appears on a webpage.
    """
    content = scrape_web(url)
    return count_word_in_text(content, word)

# Test scraping functionality
url = "https://github.com/alexeygrigorev/minsearch"
content = scrape_web(url)
print("Characters retrieved:", len(content))

# Test word counting functionality
print("\n" + "="*50)
print("Testing word counting on datatalks.club")
print("="*50)

datatalks_url = "https://datatalks.club/"
word_to_count = "data"

print(f"Counting occurrences of '{word_to_count}' on {datatalks_url}")
try:
    count = count_word_on_webpage(datatalks_url, word_to_count)
    print(f"✅ The word '{word_to_count}' appears {count} times on {datatalks_url}")
except Exception as e:
    print(f"❌ Error: {e}")