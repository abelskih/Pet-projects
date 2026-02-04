import requests

from src.api.api_urls import api_urls


def get_plans() -> dict:
    """
    Request to /plans and return dict with all cloud tariffs

    Returns:
        dict: All CG tariffs
    """
    result = requests.get(api_urls["cloud"]["plans"])
    return result.json()


def get_games(page=1, page_size=24, genres=None, plan_family_slug=None) -> list:
    """
    Return dict of games data from CLOUDGAMES API

    Args:
        page (int, optional): Page number. Defaults to 1.
        page_size (int, optional): Page size. Defaults to 24.
        genres (str, optional): Genres of games. Defaults to None.

    Returns:
        list: List of games data
    """
    payload = {
        "page": page,
        "page_size": page_size,
        "o": "-priority",
        "genres": genres,
        "plan_family_slug": plan_family_slug,
    }

    result = requests.get(api_urls["cloud"]["games"], params=payload)
    return result.json()["results"]


def get_user_quests(cookie) -> list:
    """
    Get user quests

    Args:
        cookie (_type_): Gerenated cloud user cookie

    Returns:
        list: Quests
    """
    headers = {"Cookie": cookie}
    result = requests.get(api_urls["cloud"]["quests"], headers=headers)

    return result.json()["results"]
