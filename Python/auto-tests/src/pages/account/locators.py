from selenium.webdriver.common.by import By

from src.utils.locators import Locator


class AccountPageLocators:
    LOGIN_FIELD = Locator(By.NAME, "login")
    PASSWORD_FIELD = Locator(By.NAME, "password")
    SUBMIT_BUTTON = Locator(By.CSS_SELECTOR, 'button[type="submit"]')
    MAIL_RU_AUTH_BUTTON = Locator(By.CLASS_NAME, "ph-social-btn_mailru")
    OK_AUTH_BUTTON = Locator(By.CLASS_NAME, "ph-social-btn_ok")
    SPINNER = Locator(By.CSS_SELECTOR, "[class^='spinner_block']")
