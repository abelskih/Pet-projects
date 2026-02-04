import json
from pathlib import Path
from typing import Optional
from urllib.parse import unquote

import allure
from src.api import sezam_api
from src.configs import vkplay_config
from src.pages.base_page_abstract import BasePageAbstract
from src.pages.locators import BasePageLocators
from src.utils.config import get_domain


class BasePageVKPlay(BasePageAbstract):
    cookie_names = vkplay_config.COOKIE_NAMES
    path_to_cookies = vkplay_config.path_to_cookies

    @allure.step("Открываем меню юзера (клик по аватарке)")
    def user_menu_click(self) -> None:
        self.wait_until_clickable(*BasePageLocators.USER_AVATAR).click()

    @allure.step("Переходим в Профиль")
    def go_to_profile(self) -> None:
        self.user_menu_click()
        self.wait_until_clickable(*BasePageLocators.PROFILE_BUTTON).click()

    @allure.step("Переходим в настройки профиля")
    def go_to_settings(self) -> None:
        self.user_menu_click()
        self.wait_until_clickable(*BasePageLocators.SETTINGS_BUTTON).click()

    @allure.step("Делаем логаут")
    def logout(self) -> None:
        if self.check_auth_cookie():
            self.user_menu_click()
            self.wait_until_clickable(*BasePageLocators.LOGOUT_BUTTON).click()

    @allure.step("Проверяем, что юзер не авторизован")
    def check_user_not_authenticated(self) -> bool:
        return bool(self.check_element_is_present(BasePageLocators.UNAUTHENTICATED_USER_BUTTON))

    @classmethod
    @allure.step("Обновляем cookie авторизации")
    def update_auth_cookies(cls, login: str, password: str, set_type: str = "main") -> None:
        current_cookies = cls.read_cookies_from_file()
        new_cookies = sezam_api.get_auth_cookies(login, password)

        for name in cls.cookie_names:
            if login not in current_cookies:
                current_cookies[login] = {}
            if set_type not in current_cookies[login]:
                current_cookies[login][set_type] = {}
            current_cookies[login][set_type][name] = new_cookies[name]

        cls.write_cookies_in_file(current_cookies)

    @classmethod
    def write_cookies_in_file(cls, new_cookies: dict) -> None:
        file = Path(cls.path_to_cookies)
        file.parent.mkdir(parents=True, exist_ok=True)
        with open(cls.path_to_cookies, "w") as f:
            cookies = json.dumps(new_cookies)
            f.write(cookies)
            f.close()

    @classmethod
    @allure.step("Достаём из файла cookie авторизации")
    def read_cookies_from_file(cls) -> dict[str, dict[str, dict[str, str]]]:
        if not os.path.isfile(cls.path_to_cookies):
            return {}
        with open(cls.path_to_cookies) as f:
            return json.load(f)

    @allure.step("Добавляем cookie авторизации в браузер")
    def add_auth_cookies_to_browser(self, login: str, password: str, set_type: str = "main") -> None:
        domain = get_domain()
        user_cookies = self.try_to_get_cookies_from_file(login, password, set_type)

        self.add_cookie("mc", user_cookies["mc"], domain)
        self.add_cookie("sdcs", user_cookies["sdcs"], domain)
        self.add_cookie("ssdc", user_cookies["ssdc"], domain)

    @classmethod
    def try_to_get_cookies_from_file(cls, login: str, password: str, cookie_type="main") -> dict:
        """
        Читаем файл cookies.json и пытаемся получить оттуда данные по авторизации юзера.
        Если данных не найдено, то пробуем авторизоваться, сохранить новые данные и повторяем.
        """
        try:
            return cls.read_cookies_from_file()[login][cookie_type]
        except KeyError:
            cls.update_auth_cookies(login, password)
            return cls.read_cookies_from_file()[login][cookie_type]

    def add_cookiebot_cookie(self) -> None:
        self.add_cookie("CookieConsent", vkplay_config.COOKIEBOT_COOKIE, f"{get_domain()}")

    def check_authenticated_avatar(self, timeout: Optional[int] = 10) -> bool:
        """Проверяем, что отобразился аватар авторизованного юзера"""
        if self.check_element_is_present(BasePageLocators.AUTHENTICATED_USER_AVATAR, timeout):
            return True
        elif self.check_element_is_present(BasePageLocators.MOBILE_MENU, timeout):
            self.click_button(*BasePageLocators.MOBILE_MENU_MORE_BUTTON)
            if self.check_element_is_present(BasePageLocators.MORE_BLOCK_UNAUTH_USER_BUTTON):
                return False
            self.wait_until_visible(*BasePageLocators.AUTHENTICATED_MOBILE_USER_AVATAR, timeout)
            self.click_button(*BasePageLocators.MOBILE_MENU_MORE_BUTTON)  # close menu after avatar check
            return True

        return False

    def check_auth_cookie(self) -> str:
        return self.get_cookie("mc")

    def check_user_authenticated(self) -> bool:
        return bool(self.check_authenticated_avatar() and self.check_auth_cookie())

    def find_tracker_event_in_browser_logs(self, category: str, event_name: str, logs: list) -> bool:
        """
        Поиск событий "tracker?" в логах браузера.
        Рамках одного теста проверяется несколько ивентов, то нужно дополнительно
        отправлять logs в параметры метода, т.к. после получения логов они вычищаются из памяти.
        """
        if not logs:
            logs = self.get_driver().get_log("performance")

        for entry in logs:
            try:
                message = json.loads(entry["message"])["message"]
                if message["method"] == "Network.requestWillBeSent":
                    url = unquote(message["params"]["request"]["url"])
                    if message["params"].get("type", "Other") != "Image":
                        continue
                    if "tracker?" in url and event_name in url and f'"category":"{category}"' in url:
                        return True
            except (json.JSONDecodeError, KeyError):
                continue

        return False

    @allure.step("Проверяем наличие нужного инвента в логах браузера")
    def check_event_is_sent(self, category: str, event_name: str, logs: list = None) -> bool:
        return bool(self.find_tracker_event_in_browser_logs(category, event_name, logs))

    def check_link_in_new_tab(self, expected_url: str) -> None:
        """
        Проверка открывшейся в новой вкладке ссылки после нажатия кнопки.
        Обычно используется для проверки лицензионных соглашений
        """
        self.change_tab(1)
        self.is_correct_link(expected_url)
        self.close_active_tab()
        self.change_tab(0)
