import re
from src.assets import perfume_ids
from src.utils.scraper.perfume_scraper import PerfumeScraper
from pathlib import Path
from src.utils.definitions import ASSETS_DIRECTORY
from src.service.tools.web_search import search_fragrantica_perfume
import pandas as pd

pretty_df = pd.read_pickle(Path.joinpath(ASSETS_DIRECTORY, "pretty_df.pkl"))


def retrieve_perfume_urls_based_on_reference_perfume(reference_perfume: str) -> list:
    """
    Retrieve perfume URLs based on a reference perfume.

    This function searches for perfumes related to a given reference perfume
    in the Fragrantica database and returns a list of URLs for the matching perfumes.

    Parameters
    ----------
    reference_perfume : str
        The name or identifier of the reference perfume to search for in the Fragrantica database.

    Returns
    -------
    list of str
        A list of URLs for the perfumes related to the given reference perfume.

    Examples
    --------
    >>> retrieve_perfume_urls_based_on_reference_perfume("Dior Sauvage")
    ['https://www.fragrantica.com/perfume/Dior/Sauvage-12345.html',
     'https://www.fragrantica.com/perfume/Dior/Sauvage-Elixir-67890.html']

    Todo
    ----
    1. Result ranking (based on number of ratings or SEO?)
    """
    results = search_fragrantica_perfume(reference_perfume)["results"]
    return [result["url"] for result in results]


def is_perfume_id_in_our_database(perfume_id: str):
    """
    Check if a given perfume ID is present in the database (actually a reference list).

    Parameters
    ----------
    perfume_id : str
        The perfume ID to check.

    Returns
    -------
    bool
        True if the perfume ID is found in the database, False otherwise.

    Examples
    --------
    >>> is_perfume_id_in_our_database('12345')
    True
    >>> is_perfume_id_in_our_database('99999')
    False
    """
    return perfume_id in perfume_ids


def _extract_id_from_url(perfume_url: str) -> str:
    """
    Extract the perfume ID from a given perfume URL.
    """
    return re.findall(r"(\d+)(?=\.html$)", perfume_url)[0]


def _extract_alias_from_url(perfume_url: str) -> str:
    """
    Extract the alias (brand and name) from a given perfume URL.

    The alias is formed by extracting the brand and name from the URL, replacing
    hyphens with spaces, and then formatting them into a string.

    Parameters
    ----------
    perfume_url : str
        The URL of the perfume on Fragrantica.

    Returns
    -------
    str
        The formatted alias, combining the brand and name.

    Example
    -------
    For the URL `https://www.fragrantica.com/perfume/Acqua-di-Parma/Magnolia8-In45finita-75188.html`,
    the returned alias will be `"[Acqua di Parma] Magnolia8 In45finita"`.
    """
    brand = re.findall(
        r"https:\/\/www\.fragrantica\.com\/perfume\/([^\/]+)", perfume_url
    )[0].replace("-", " ")
    name = re.findall(
        r"https:\/\/www\.fragrantica\.com\/perfume\/[^\/]+\/([^\/-]+(?:-[^\/]+)*)(?=-\d+\.html)",
        perfume_url,
    )[0].replace("-", " ")
    return f"[{brand}] {name}"


def scrape_perfume_details_via_url(perfume_url: str) -> dict:
    """
    Scrape perfume details from a given URL using an instantiated `PerfumeScraper`.

    This function creates a `PerfumeScraper` object to extract various perfume details,
    including ID, alias, accords, notes, and rating, based on the provided URL.

    Parameters
    ----------
    perfume_url : str
        The URL of the perfume on Fragrantica.

    Returns
    -------
    dict
        A dictionary containing extracted perfume details, such as ID, alias, accords,
        notes (top, middle, and base), and rating. The keys are consistent with the structure
        of `pretty_df`.

    Example
    -------
    For a given perfume URL, the returned dictionary will have the following keys:
    - "ID": Extracted perfume ID
    - "Alias": Extracted alias (brand and name)
    - "Accords": List of accords
    - "Notes": List of notes
    - "Top Notes": List of top notes
    - "Middle Notes": List of middle notes
    - "Base Notes": List of base notes
    - "Rating": Extracted rating
    """
    scraper = PerfumeScraper(perfume_url)
    return {  # Same keys as in pretty_df
        "ID": scraper.extract_id(),
        "Alias": _extract_alias_from_url(perfume_url),
        "Accords": scraper.extract_accords(),
        "Notes": scraper.extract_notes(),
        "Top Notes": scraper.notes["top"],
        "Middle Notes": scraper.notes["middle"],
        "Base Notes": scraper.notes["base"],
        "Rating": scraper.extract_rating_info()["Rating"],
    }


def retrieve_perfume_details_based_on_perfume_url(perfume_url) -> dict:
    """
    Retrieve perfume details for a given perfume URL.

    This function checks if the perfume ID is already present in the database. If so,
    it returns the corresponding details from `pretty_df`. Otherwise, it scrapes the details
    using the provided URL.

    Parameters
    ----------
    perfume_url : str
        The URL of the perfume on Fragrantica.

    Returns
    -------
    dict
        A dictionary containing perfume details. If the ID is found in the database,
        it returns the details from `pretty_df`, otherwise, it scrapes the details from
        the URL.

    Example
    -------
    For a given perfume URL, the returned dictionary will have keys like:
    - "ID": Extracted perfume ID
    - "Alias": Extracted alias (brand and name)
    - "Accords": List of accords
    - "Notes": List of notes
    - "Top Notes": List of top notes
    - "Middle Notes": List of middle notes
    - "Base Notes": List of base notes
    - "Rating": Extracted rating
    """
    perfume_id = _extract_id_from_url(perfume_url)
    if is_perfume_id_in_our_database(perfume_id=perfume_id):
        return pretty_df.loc[perfume_id, :].to_dict()
    else:
        return scrape_perfume_details_via_url(perfume_url)


def retrieve_perfume_details_based_on_perfume_urls(perfume_urls: list) -> list:
    """
    Retrieve perfume details for a list of perfume URLs.

    This function iterates over a list of perfume URLs and fetches the details for each URL
    by calling `retrieve_perfume_details_based_on_perfume_url`.

    Parameters
    ----------
    perfume_urls : list of str
        A list of URLs of perfumes on Fragrantica.

    Returns
    -------
    list of dict
        A list of dictionaries, where each dictionary contains the details of a perfume
        corresponding to the provided URLs.

    Example
    -------
    >>> retrieve_perfume_details_based_on_perfume_urls([
    >>>     'https://www.fragrantica.com/perfume/Dior/Sauvage-12345.html',
    >>>     'https://www.fragrantica.com/perfume/Dior/Sauvage-Elixir-67890.html'
    >>> ])
    [{'ID': 12345, 'Alias': 'Dior Sauvage', 'Accords': [...], 'Notes': [...], ...},
     {'ID': 67890, 'Alias': 'Dior Sauvage Elixir', 'Accords': [...], 'Notes': [...], ...}]
    """
    return [
        retrieve_perfume_details_based_on_perfume_url(perfume_url)
        for perfume_url in perfume_urls
    ]


def retrieve_data_based_on_reference_perfume(reference_perfume):
    """
    Retrieve perfume details for a reference perfume.

    This function first retrieves a list of perfume URLs related to the reference perfume
    and then fetches the details for each URL.

    Parameters
    ----------
    reference_perfume : str
        The name or identifier of the reference perfume.

    Returns
    -------
    list of dict
        A list of dictionaries containing perfume details for all the perfumes related
        to the reference perfume.

    Example
    -------
    >>> retrieve_data("Dior Sauvage")
    [{'ID': 12345, 'Alias': 'Dior Sauvage', 'Accords': [...], 'Notes': [...], ...},
     {'ID': 67890, 'Alias': 'Dior Sauvage Elixir', 'Accords': [...], 'Notes': [...], ...}]
    """
    perfume_urls = retrieve_perfume_urls_based_on_reference_perfume(
        reference_perfume=reference_perfume
    )
    return retrieve_perfume_details_based_on_perfume_urls(perfume_urls=perfume_urls)
