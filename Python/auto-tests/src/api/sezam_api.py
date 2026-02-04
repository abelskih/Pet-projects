import requests
from requests import Session

import allure
import src.api.api_urls as api


@allure.step("Создаем сессию для юзера")
def get_session_for_user(cookies: dict[str, str]) -> Session:
    s = requests.Session()
    s.cookies.update(cookies)
    s.get(api.SEZAM_AUTH_LINK + "sdc", params={"from": api.API_HOST})
    return s


@allure.step("Getting authorization cookies")
def get_auth_cookies(login: str, password: str) -> dict[str, str]:
    """
    Getting authorization cookies
    :param login:
    :param password:
    :return:
    """
    header = {"Content-Type": "application/json"}
    session = requests.Session()

    init_response = session.post(
        api.api_urls["sezam"]["auth_link"] + "init",
        headers=header,
        json={"login": login},
        allow_redirects=True,
    )
    init_data = init_response.json()
    token = init_data["token"]

    verify_response = session.post(
        api.api_urls["sezam"]["auth_link"] + "verify",
        headers=header,
        json={"token": token, "login": login, "password": password},
    )
    auth_redirect = verify_response.json()["auth_redirect"]

    session.get(auth_redirect)

    cookies = session.cookies.get_dict()
    return cookies
