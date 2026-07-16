import wikipediaapi

def search_wikipedia(query: str) -> str:
    """
    Searches Wikipedia for the given query and returns a short summary of the page.
    """
    # Wikipedia strictly requires a custom User-Agent to avoid blocking requests.
    # We use a real identifier with your name/email as the contact.
    wiki = wikipediaapi.Wikipedia(
        user_agent="DanielBasaznewAgent/1.0 (danielbasaznew@gmail.com)",
        language="en"
    )
    
    try:
        # Clean up the query string
        clean_query = query.strip()
        page = wiki.page(clean_query)
        
        # Check if the page exists
        if not page.exists():
            return f"[OBSERVATION]: No Wikipedia page found for '{clean_query}'. Try a different search term."
            
        # Extract the summary and truncate it to keep our token context window small
        summary = page.summary
        if len(summary) > 500:
            return summary[:500] + "..."
            
        return summary
        
    except Exception as e:
        return f"[OBSERVATION Error]: Failed to search Wikipedia. Details: {e}"