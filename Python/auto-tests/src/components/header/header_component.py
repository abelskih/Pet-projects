from src.components.header.locators import HeaderComponentLocators
from src.pages.base_page_vkplay import BasePageVKPlay


class HeaderComponent(BasePageVKPlay):
    def __init__(self, app, url):
        super().__init__(app, url)

    def click_navigation_button(self, section_name: str):
        self.try_to_click_button(*HeaderComponentLocators.locators_dict[section_name]["nav_button"])
