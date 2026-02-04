from selenium.webdriver.common.by import By

from src.utils.locators import Locator


class BasePageLocators:
    AUTHENTICATED_USER_AVATAR = Locator(By.CSS_SELECTOR, "button[class^='_profileButton'] > img[class^='_avatar']")

    LANGUAGE_ICON = Locator(By.XPATH, '//span[contains(@class, "icon_lang")]')
    LANGUAGE_DROPDOWN = Locator(By.CLASS_NAME, "ph-dropdown__default_desktop")
    LANGUAGE_RU = Locator(By.XPATH, '//a[text()="Русский"]')
    LANGUAGE_DROPDOWN_EN = Locator(By.XPATH, '//a[text()="English"]')
    NOTIFICATIONS_ICON = Locator(By.CSS_SELECTOR, "[data-tooltip-id='notification-notifications']")
    ACCEPT_FRIEND_IN_NOTIFICATION_BUTTON = Locator(
        By.CSS_SELECTOR, "#notification-notifications [class^='_actions'] > button[class*='_mode-primary']"
    )
    NOTIFICATIONS_FRINED_ADDED_NOTIFICATION = Locator(
        By.CSS_SELECTOR, "#notification-notifications [class^='_notificationLabel']"
    )
    USER_AVATAR = Locator(By.CSS_SELECTOR, "button[class^='_profileButton']")
    LOGOUT_BUTTON = Locator.data_test("logout_link")
    PROFILE_BUTTON = Locator(By.CSS_SELECTOR, "a[class^='_toProfile']")
    SETTINGS_BUTTON = Locator(By.CSS_SELECTOR, "[class^='_profileLinks'] > [class^='_link']")
    UNAUTHENTICATED_USER_BUTTON = Locator(By.CSS_SELECTOR, "div[class^='_container'] > a[class^='_button']")
    COOKIEBOT_ACCEPT = Locator(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
    MOBILE_MENU = Locator(By.CSS_SELECTOR, "div[class^='_containerMob']")
    MOBILE_MENU_MORE_BUTTON = Locator(By.CSS_SELECTOR, "button[data-id='more']")
    MORE_BLOCK_UNAUTH_USER_BUTTON = Locator(By.CSS_SELECTOR, "div[class^='_noAuthContent'] > a[class^='_button']")
    AUTHENTICATED_MOBILE_USER_AVATAR = Locator(By.CSS_SELECTOR, "div[class^='_authHeader'] > div[class^='_avatar']")

    PARENT_ELEMENT = Locator(By.XPATH, "./..")
    NEXT_ELEMENT = Locator.xpath(".//following-sibling::*[1]")
    INPUT = Locator(By.TAG_NAME, "input")
