from src.pages.base_page_vkplay import BasePageVKPlay
from src.pages.cloud.locators import LandingPageLocators


class LandingPage(BasePageVKPlay):
    def check_landing_blocks_are_shown(self) -> bool:
        self.wait_until_visible(*LandingPageLocators.ROOT_ROUTES)
        for block in LandingPageLocators.blocks_to_landing_is_loaded_check:
            self.wait_until_visible(*block)
        return True

    def check_content_is_loaded(self, block_name: str, content_block_name: str) -> bool:
        """
        Check the block and the content attached to the block. Content usually refers to an image or video

        Args:
            block_name (str): Block name to take locator from blocks dict
            content_block_name (str): Content block name to take locator from blocks dict
        """
        self.wait_until_visible(*LandingPageLocators.landing_blocks[block_name])
        self.wait_until_multiple_visible(*LandingPageLocators.landing_blocks[content_block_name])
        return True

    def check_direct_download_buttons_in_block(self, block_name: str) -> list:
        """
        Get href attribute of download buttons

        Args:
            block_name (str): Block name to take locator from blocks dict
        """
        block = self.wait_until_visible(*LandingPageLocators.landing_blocks[block_name])
        buttons = block.find_elements(*LandingPageLocators.DOWNLOAD_DIRECT_BUTTONS)
        return [buttons[0].get_attribute("href"), buttons[1].get_attribute("href")]

    def check_popup_download_buttons_click(self, block_name: str, button_number: int) -> dict:
        """
        Open pop-up and return href values for checks:
        direct apk download button and button with _blank href, that opens new tab in browser.

        Args:
          block_name (str): Expected block with pop-up buttons
          button_number (int): Button number in block from block_locator arg
        """
        block = self.wait_until_visible(*LandingPageLocators.landing_blocks[block_name])
        button = block.find_elements(*LandingPageLocators.DOWNLOAD_POPUP_BUTTONS)[button_number]
        button.click()
        self.wait_until_visible(*LandingPageLocators.POPUP_ANDROID_DOWNLOAD)
        direct_download_button = self.wait_until_visible(*LandingPageLocators.POPUP_DIRECT_APK_DOWNLOAD_BUTTON)
        store_buttons = self.wait_until_multiple_visible(*LandingPageLocators.POPUP_GOOGLE_PLAY_DOWNLOAD_BUTTON)
        direct_href = direct_download_button.get_attribute("href")
        store_hrefs = [btn.get_attribute("href") for btn in store_buttons]
        return {"direct": direct_href, "stores": store_hrefs}

    def click_button_on_landing(self, button_name: str) -> None:
        """
        Get locator by button name and click button with that locator

        Args:
            button_name (str): Button name in landing_blocks dict
        """
        self.wait_until_visible(*LandingPageLocators.landing_blocks[button_name])
        self.click_button(*LandingPageLocators.landing_blocks[button_name])
