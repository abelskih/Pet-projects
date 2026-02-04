from selenium.webdriver.remote.webelement import WebElement

from src.components.plan_selector.locators import PlanSelectorComponentLocators
from src.pages.base_page_abstract import BasePageAbstract
from src.utils import convert_price_text_to_num, trim_text_after_symbol
from src.utils.locators import Locator


class PlanSelectorComponent(BasePageAbstract):
    def __init__(self, app, url):
        super().__init__(app, url)

    def switch_plans_tab(self, button_locator: Locator, expected_block_locator: Locator) -> None:
        """
        Switching the tariff type and checking the switching result

        Args:
          button_locator (Locator): Button locator in the tariff switch block
          expected_block_locator (Locator): Expected block to be displayed after the button is clicked.
        """
        button = self.wait_until_visible(*button_locator)
        button.click()
        self.wait_until_visible(*expected_block_locator)

    def switch_plans_to_hours_tab(self) -> None:
        self.switch_plans_tab(PlanSelectorComponentLocators.TAB_HOURS, PlanSelectorComponentLocators.RANGE_ROOT)

    def switch_plans_to_months_tab(self) -> None:
        self.switch_plans_tab(PlanSelectorComponentLocators.TAB_MONTHS, PlanSelectorComponentLocators.MONTHS_CALC)

    def get_plan_items_from_page(self) -> list:
        return self.wait_until_multiple_visible(*PlanSelectorComponentLocators.PLAN_ITEM)

    def is_selected_plan_time_correct(self, locator: Locator, item: WebElement) -> bool:
        """
        Comparison of time of allocated tariff plan from landing slider and tariff time from API

        Args:
          locator (Locator): Locator to selected plan block
          item (WebElement): Current parsed item from page
        """
        return bool(self.wait_until_text(*locator, text=item.text))

    def get_int_price_from_element(self, element: WebElement, replace_str=" ₽") -> int:
        """
        Get price string from web page

        Args:
          element (WebElement): block with price
          replace_str (str): What to remove from the raw string

        Returns:
          int: Price in numeric format
        """
        raw_price_text = element.text
        trimmed_price_text = trim_text_after_symbol(raw_price_text, "₽")
        return convert_price_text_to_num(trimmed_price_text, replace_str)

    def get_selected_plan_name(self) -> str:
        """
        Get selected plan value (hours) and label from page and return it in string format

        Returns:
          str: Full plan name
        """
        plan_value = self.wait_until_visible(*PlanSelectorComponentLocators.SELECTED_ITEM_VALUE).text
        plan_hours_label = self.wait_until_visible(*PlanSelectorComponentLocators.SELECTED_ITEM_HOURS_TEXT).text
        return f"{plan_value} {plan_hours_label}"

    def get_hour_plans_ui_data(self) -> list:
        """
        Switch to hours tab and return UI data for each plan.
        """
        self.switch_plans_to_hours_tab()
        plan_items = self.get_plan_items_from_page()
        data = []

        for i in range(len(plan_items)):
            page_plans = self.get_plan_items_from_page()
            page_plans[i].click()
            page_plan = self.get_plan_items_from_page()[i]
            self.is_selected_plan_time_correct(PlanSelectorComponentLocators.SELECTED_ITEM_VALUE, page_plan)
            selected_plan_name = self.get_selected_plan_name()
            selected_item_price = self.wait_until_visible(*PlanSelectorComponentLocators.SELECTED_ITEM_PRICE)
            selected_price = self.get_int_price_from_element(selected_item_price)

            old_price = None
            old_price_element = self.check_element_is_present(
                PlanSelectorComponentLocators.SELECTED_ITEM_OLD_PRICE, timeout=1, clickable=False
            )
            if old_price_element:
                old_price = self.get_int_price_from_element(old_price_element)

            data.append(
                {
                    "name": selected_plan_name,
                    "price": selected_price,
                    "old_price": old_price,
                    "minutes_text": page_plan.text,
                }
            )

        return data

    def get_month_plans_ui_data(self) -> list:
        """
        Switch to months tab and return UI data for each plan card.
        """
        self.switch_plans_to_months_tab()
        cards = self.wait_until_multiple_visible(*PlanSelectorComponentLocators.MONTHS_CARD)
        data = []
        for card in cards:
            plan_name = card.find_element(*PlanSelectorComponentLocators.MONTHS_CARD_NAME).text
            current_plan_card = card.find_element(*PlanSelectorComponentLocators.MONTHS_PRICE)
            month_price = self.get_int_price_from_element(current_plan_card)
            old_price = None
            try:
                current_plan_old_price = card.find_element(*PlanSelectorComponentLocators.MONTHS_OLD_PRICE)
                old_price = self.get_int_price_from_element(current_plan_old_price)
            except Exception:
                old_price = None

            data.append({"name": plan_name, "price": month_price, "old_price": old_price})

        return data

    def click_month_plan_button(self, card_number: int) -> None:
        """
        Switch plans to months tab and button in a certain tariff card

        Args:
          card_number (int): Card number on the page
        """
        self.switch_plans_to_months_tab()
        cards = self.wait_until_multiple_visible(*PlanSelectorComponentLocators.MONTHS_CARD)
        button = cards[card_number].find_element(*PlanSelectorComponentLocators.BUTTON_BLOCK)
        button.click()
