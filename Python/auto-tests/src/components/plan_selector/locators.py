from selenium.webdriver.common.by import By

from src.utils.locators import Locator


class PlanSelectorComponentLocators:
    TAB_HOURS = Locator(By.ID, "hoursPlanTab")
    TAB_MONTHS = Locator(By.ID, "monthsPlanTab")
    RANGE_ROOT = Locator(By.CSS_SELECTOR, "[class^='plans-range_root']")
    PLAN_ITEM = Locator(By.CSS_SELECTOR, "[class^='plans-range_planItem']")
    SELECTED_ITEM_VALUE = Locator(By.CSS_SELECTOR, "[class^='plans-range_runnerValue']")
    SELECTED_ITEM_HOURS_TEXT = Locator(By.CSS_SELECTOR, "[class^='plans-range_runnerHours']")
    SELECTED_ITEM_PRICE = Locator(By.CSS_SELECTOR, "[class^='plans-hours-calc_currentPrice']")
    SELECTED_ITEM_OLD_PRICE = Locator(By.CSS_SELECTOR, "[class^='plans-hours-calc_oldPrice']")
    MONTHS_CALC = Locator(By.CSS_SELECTOR, "[class^='plans-months-calc_plansWrap']")
    MONTHS_CARD = Locator(By.CSS_SELECTOR, "[class^='PlanTile_container']")
    MONTHS_CARD_NAME = Locator(By.CSS_SELECTOR, "[class^='PlanTile_name']")
    MONTHS_PRICE = Locator(By.CSS_SELECTOR, "[class^='PlanTile_planPrice'] > [class^='text_block']")
    MONTHS_OLD_PRICE = Locator(By.CSS_SELECTOR, "[class*='PlanTile_buttonOldPrice']")
    BUTTON_BLOCK = Locator(By.CSS_SELECTOR, "[class^='button_block']")
