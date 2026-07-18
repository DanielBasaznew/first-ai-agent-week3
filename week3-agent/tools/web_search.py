import time
from ddgs import DDGS  # Upgraded library reference

def search_web(query: str) -> str:
    """
    Searches the live web using the updated DDGS library.
    Uses the stable text scraping backend to bypass anti-bot locks.
    """
    clean_query = query.strip().strip('"').strip("'")
    
    try:
        with DDGS() as ddgs:
            # FIX: Changed 'keywords=' to 'query=' to match the new package signature
            results = list(ddgs.text(query=clean_query, max_results=3, backend="lite"))
            
        if not results:
            return f"[OBSERVATION]: Web search returned no results for '{clean_query}'."
            
        formatted_results = []
        for i, res in enumerate(results, start=1):
            title = res.get('title', 'No Title')
            body = res.get('body', 'No Description available.')
            url = res.get('href', 'No URL')
            
            formatted_results.append(f"{i}. Title: {title}\n   Snippet: {body}\n   URL: {url}")
            
        return "\n\n".join(formatted_results)
        
    except Exception as e:
        return f"[OBSERVATION Error]: Web search failed. Details: {e}"

# FIX: Added double underscores so the local test block executes correctly
if __name__ == "__main__":
    print(search_web("the current prime minster of Ethiopia"))