import os
from tavily import TavilyClient

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_fragrantica_subdirectory(subdirectory: str, query: str):
    """
    Perform a search within a specific Fragrantica subdirectory.

    Parameters
    ----------
    subdirectory : str
        The subdirectory of the Fragrantica website to search (e.g., "forum", "news", "perfume").
    query : str
        The search query to execute.

    Returns
    -------
    list
        A list of search results returned by the Tavily client.
    """
    print(f"Doing {subdirectory} search for {query}...")
    return tavily_client.search(f"site:fragrantica.com/{subdirectory} {query}")


# Note: partial functions do not work with swarm because it needs __name__ attribute for tools
def search_fragrantica_forum(query: str):
    """
    Perform a search within Fragrantica's forum subdirectory.

    Parameters
    ----------
    query : str
        The search query to execute.
    """
    return search_fragrantica_subdirectory(subdirectory="forum", query=query)


def search_fragrantica_notes(query: str):
    """
    Perform a search within Fragrantica's notes subdirectory.

    Parameters
    ----------
    query : str
        The search query to execute.
    """
    return search_fragrantica_subdirectory(subdirectory="notes", query=query)


def search_fragrantica_news(query: str):
    """
    Perform a search within Fragrantica's news subdirectory.

    Parameters
    ----------
    query : str
        The search query to execute.
    """
    return search_fragrantica_subdirectory(subdirectory="news", query=query)


def search_fragrantica_perfume(query: str):
    """
    Perform a search within Fragrantica's perfume subdirectory.

    Parameters
    ----------
    query : str
        The search query to execute.
    """
    return search_fragrantica_subdirectory(subdirectory="perfume", query=query)
