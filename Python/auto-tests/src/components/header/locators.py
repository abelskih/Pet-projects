from src.utils.locators import Locator


class HeaderComponentLocators:
    LOGIN_BUTTON = Locator.data_id("login-button")

    locators_dict = {
        "auth": {
            "nav_button": LOGIN_BUTTON,
        },
    }
