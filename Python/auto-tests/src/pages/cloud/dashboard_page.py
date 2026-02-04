import os
from urllib.parse import urlparse

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

import allure
from src.pages.base_page_vkplay import BasePageVKPlay
from src.pages.cloud.locators import DashboardPageLocators as Locators
from src.utils.config import get_domain


class DashboardPage(BasePageVKPlay):
    def get_filename_from_url(self, url: str) -> str:
        """Парсим название файла из url"""
        parsed_url = urlparse(url)
        path = parsed_url.path
        filename = os.path.basename(path)
        return str(filename)

    def parse_card_data(self, card: WebElement) -> dict:
        """Парсим данные из карточки с игрой на странице"""
        try:
            age_limit = card.find_element(*Locators.GAMECARD_AGELIMIT).get_attribute("textContent").replace("+", "")
        except NoSuchElementException:
            age_limit = ""

        return {
            "name": card.find_element(*Locators.GAMECARD_NAME).get_attribute("textContent"),
            "descr": card.find_element(*Locators.GAMECARD_DESCRIPTION).get_attribute("textContent"),
            "genre_descr": card.find_element(*Locators.GAMECARD_GENRE).get_attribute("textContent"),
            "age_limit": age_limit,
            "picture": card.find_element(*Locators.IMG).get_attribute("src"),
        }

    @allure.step("Получаем все карточки игр со страницы и проверяем, что они не пустые")
    def get_catalog_cards(self) -> list:
        catalog_cards = self.wait_until_multiple_visible(*Locators.CATALOG_GAMECARD_BLOCK)
        return catalog_cards

    def is_dashboard_block_visible(self, locator_name: str) -> bool:
        self.wait_until_visible(*Locators.dashboard_blocks[locator_name])
        return True

    def get_catalog_cards_data(self) -> list:
        catalog_cards = self.get_catalog_cards()
        return [self.parse_card_data(card) for card in catalog_cards]

    @allure.step("Ищем игру в поиске")
    def search_game_by_name(self, text: str):
        self.wait_until_visible(*Locators.SEARCH_BLOCK)
        self.send_input_value(*Locators.SEARCH_INPUT, text)

    @allure.step("Проверяем результаты поиска")
    def check_search_result(self, text) -> bool:
        return bool(self.wait_until_text(*Locators.GAMECARD_NAME, text))

    @allure.step("Ждём пустой результат поиска")
    def check_is_empty_search_result_shown(self) -> bool:
        self.wait_until_visible(*Locators.CATALOG_SEARCH_EMPTY)
        return True

    @allure.step("Проверяем, что шапку дашборда не видно")
    def check_dashboard_header_is_visible(self) -> bool:
        self.wait_until_visible(*Locators.DASHBOARD_HEADER)
        return True

    @allure.step("Проверяем, что шапку дашборда видно")
    def check_dashboard_header_is_not_visible(self) -> bool:
        return bool(self.wait_until_not_visible(*Locators.DASHBOARD_HEADER))

    def click_dashboard_button(self, button_name: str):
        self.click_button(*Locators.dashboard_blocks[button_name])

    def get_cloud_sdcs_cookie(self) -> str:
        """
        Get cloudgaming sdcs cookie from all cookies and return it

        Raises:
            Exception: Cookie not found in all cookies

        Returns:
            str: cloud sdcs cookie
        """
        for cookie in self.get_driver().get_cookies():
            if cookie["domain"] == f".cloud{get_domain()}" and cookie["name"] == "sdcs":
                return cookie["value"]

        raise Exception("Can't find cloud sdcs cookie")

    def create_header_cookie_for_cloud_request(self, login) -> str:
        """
        Create header for cloudgaming api request. Necessary to work with the data of a particular user.

        Args:
            login (_type_): user login

        Returns:
            str: header data
        """
        main_mc_cookie = self.read_cookies_from_file()[login]["main"]["mc"]
        cloud_sdcs_cookie = self.get_cloud_sdcs_cookie()
        return f"mc={main_mc_cookie};sdcs={cloud_sdcs_cookie}"

    def get_task_cards_data(self) -> list:
        all_plan_cards = self.wait_until_multiple_visible(*Locators.PLAN_CARD)
        data = []
        for plan_card in all_plan_cards:
            card_plan_name = plan_card.find_element(*Locators.PLAN_NAME_BLOCK).text
            bg_picture = plan_card.find_element(*Locators.PLAN_BACK).get_attribute("style")
            data.append({"name": card_plan_name, "bg_picture": bg_picture})
        return data

    def get_buttons_from_block(self, block_locator: str) -> list:
        """
        Get download <a> buttons from some block

        Args:
            block_locator (str):

        Returns:
            list: list of WebElements with buttons
        """
        block = self.wait_until_visible(*Locators.dashboard_blocks[block_locator])
        return block.find_elements(*Locators.DOWNLOAD_BUTTONS_IN_BLOCK)

    @allure.step("Открываем фильтр в каталоге")
    def open_filter_block(self) -> None:
        self.try_to_click_button(*Locators.FILTERS_BUTTON)

    @allure.step("Выбираем фильтр -> Входят в тариф")
    def select_tariff(self, button_name: str) -> None:
        self.click_button(*Locators.dashboard_blocks[button_name])

    @allure.step("Выбираем жанр -> MMO")
    def select_mmo_genre(self) -> None:
        self.click_button(*Locators.FILTER_MMO_GENRE)

    @allure.step("Закрываем фильтр каталога")
    def close_filter_block(self) -> None:
        self.click_button(*Locators.FILTERS_BACK_BUTTON)

    def click_show_button(self) -> None:
        self.click_button(*Locators.FILTERS_SHOW_BUTTON)

    @allure.step("Сбрасываем фильтр")
    def reset_all_filters(self) -> None:
        self.click_button(*Locators.FILTERS_RESET_BUTTON)
