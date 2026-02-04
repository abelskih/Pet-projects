from selenium.webdriver.common.by import By

from src.utils.locators import Locator


class LandingPageLocators:
    ROOT_ROUTES = Locator(By.CLASS_NAME, "RootRoutes")
    MAIN_BLOCK = Locator(By.CSS_SELECTOR, "[class^='LandingMain_root']")
    MAIN_BLOCK_PLAY_BUTTON = Locator(By.CSS_SELECTOR, "[class^='LandingMain_content'] > [class^='button_block']")
    FEATURES_BLOCK = Locator(By.CSS_SELECTOR, "[class^='features_block']")
    FEATURES_ITEMS_IMG = Locator(By.CSS_SELECTOR, "[class^='feature-item_icon']")
    GAMES_BLOCK = Locator(By.CSS_SELECTOR, "[class^='games_block']")
    GAMES_BLOCK_PLAY_BUTTON = Locator(By.CSS_SELECTOR, "[class^='games_block'] [class^='button_block']")
    PLANS_BLOCK = Locator(By.CSS_SELECTOR, "[class^='landing-plans-block_container']")
    PLANS_BLOCK_PLAY_BUTTON = Locator(By.CSS_SELECTOR, "[class*='plans-hours-calc_buyButton']")
    ABOUT_BLOCK = Locator(By.CSS_SELECTOR, "[class^='about_block']")
    ABOUT_BLOCK_IMGS = Locator(By.CSS_SELECTOR, "[class^='about_devices'] img")
    VIDEO_COMPARSION_BLOCK = Locator(By.CSS_SELECTOR, "[class^='VideoComparisonSlider_block']")
    VIDEO_COMPARSION_VIDEO = Locator(By.CSS_SELECTOR, "[class^='VideoComparisonSlider_block'] video")
    ANY_MACHINE_ACTION_BLOCK = Locator(By.CSS_SELECTOR, "[class^='any-machine-vkplay_action']")
    ANY_MACHINE_BLOCK_PLAY_BUTTON = Locator(
        By.CSS_SELECTOR, "[class^='any-machine-vkplay_action'] > [class^='button_block']"
    )
    ANY_MACHINE_BLOCK = Locator(By.CSS_SELECTOR, "[class^='any-machine-vkplay_bgWrap']")
    ANY_MACHINE_BG = Locator(By.CSS_SELECTOR, "[class^='any-machine-vkplay_bg']")
    DOWNLOAD_DIRECT_BUTTONS = Locator(By.CSS_SELECTOR, "a[class^='badge-support_noDecoration']")
    DOWNLOAD_POPUP_BUTTONS = Locator(By.CSS_SELECTOR, "div > [class^='badge-support_badgeBlock']")
    POPUP_ANDROID_DOWNLOAD = Locator(By.CSS_SELECTOR, "[class^='ModalDownloadAndroidApp_block']")
    POPUP_GOOGLE_PLAY_DOWNLOAD_BUTTON = Locator(By.CSS_SELECTOR, "a[class^='ModalDownloadAndroidApp_noDecoration']")
    POPUP_DIRECT_APK_DOWNLOAD_BUTTON = Locator(By.CSS_SELECTOR, "a[class^='button_block']")
    FAQ_BLOCK = Locator(By.CSS_SELECTOR, "[class^='faq_block']")
    LAUNCH_BLOCK = Locator(By.CSS_SELECTOR, "[class^='launch_block']")
    LAUNCH_BLOCK_PLAY_BUTTON = Locator(By.CSS_SELECTOR, "[class^='launch_action'] > [class^='button_block']")
    BUTTON_BLOCK = Locator(By.CSS_SELECTOR, "[class^='button_block']")
    TEXT_BLOCK = Locator(By.CSS_SELECTOR, "[class^='text_block']")
    SOCIAL_VK_BUTTON = Locator(By.CSS_SELECTOR, "[data-testid='ui-icon-vk']")
    SOCIAL_DISCORD_BUTTON = Locator(By.CSS_SELECTOR, "[data-testid='ui-icon-discord']")

    landing_blocks = {
        "ABOUT_BLOCK": ABOUT_BLOCK,
        "ABOUT_BLOCK_IMGS": ABOUT_BLOCK_IMGS,
        "FEATURES_BLOCK": FEATURES_BLOCK,
        "FEATURES_ITEMS_IMG": FEATURES_ITEMS_IMG,
        "VIDEO_COMPARSION_BLOCK": VIDEO_COMPARSION_BLOCK,
        "VIDEO_COMPARSION_VIDEO": VIDEO_COMPARSION_VIDEO,
        "ANY_MACHINE_BLOCK": ANY_MACHINE_BLOCK,
        "ANY_MACHINE_BG": ANY_MACHINE_BG,
        "GAMES_BLOCK_PLAY_BUTTON": GAMES_BLOCK_PLAY_BUTTON,
        "SOCIAL_VK_BUTTON": SOCIAL_VK_BUTTON,
        "MAIN_BLOCK_PLAY_BUTTON": MAIN_BLOCK_PLAY_BUTTON,
        "PLANS_BLOCK_PLAY_BUTTON": PLANS_BLOCK_PLAY_BUTTON,
        "ANY_MACHINE_BLOCK_PLAY_BUTTON": ANY_MACHINE_BLOCK_PLAY_BUTTON,
        "LAUNCH_BLOCK_PLAY_BUTTON": LAUNCH_BLOCK_PLAY_BUTTON,
    }

    blocks_to_landing_is_loaded_check = [
        MAIN_BLOCK,
        FEATURES_BLOCK,
        GAMES_BLOCK,
        PLANS_BLOCK,
        ABOUT_BLOCK,
        VIDEO_COMPARSION_BLOCK,
        ANY_MACHINE_ACTION_BLOCK,
        ANY_MACHINE_BLOCK,
        FAQ_BLOCK,
        LAUNCH_BLOCK,
    ]


class DashboardPageLocators:
    CONTENT_BLOCK = Locator.id("hintContentAnchor")
    SEARCH_BLOCK = Locator.id("searchHint")
    SEARCH_INPUT = Locator.id("searchInput")
    CATALOG_BLOCK = Locator.class_starts_with("Catalog_block")
    CATALOG_GAMECARD_BLOCK = Locator.class_starts_with("item-card_block")
    CATALOG_SEARCH_EMPTY = Locator.class_starts_with("catalog-empty_block")
    GAMECARD_NAME = Locator.class_starts_with("item-card_name")
    GAMECARD_DESCRIPTION = Locator.class_starts_with("item-card_description")
    GAMECARD_AGELIMIT = Locator.class_starts_with("item-card_ageLimit")
    GAMECARD_GENRE = Locator.class_starts_with("item-card_genre")
    TASKS_CONTENT_BLOCK = Locator.class_starts_with("tasks_content")
    PLANS_CONTENT_BLOCK = Locator.class_starts_with("plan-change_root")
    PLAN_CARD = Locator.class_starts_with("TaskCard_root")
    PLAN_NAME_BLOCK = Locator.class_starts_with("text_block")
    PLAN_BACK = Locator.class_starts_with("TaskCard_back")
    SETTINGS_CONTENT_BLOCK = Locator.class_starts_with("settings_block")
    DOWNLOAD_CONTENT_BLOCK = Locator.class_starts_with("download_root")
    DOWNLOAD_MOBILE_BLOCK = Locator(By.CSS_SELECTOR, "[class*='download_mobileBlock']")
    DOWNLOAD_TV_BLOCK = Locator(By.CSS_SELECTOR, "[class*='download_tvBlock']")
    DOWNLOAD_BUTTONS_IN_BLOCK = Locator.css("a[class*='download_link']")
    FAQ_CONTENT_BLOCK = Locator.class_starts_with("faq_root")
    IMG = Locator(By.TAG_NAME, "img")
    DASHBOARD_HEADER = Locator.css("div[class^='_subnav'] > [class^='_menu']")
    D_HEADER_MAIN = Locator.id("eva-subnav-1")
    D_HEADER_TASKS = Locator.id("eva-subnav-2")
    D_HEADER_PLANS = Locator.id("eva-subnav-3")
    D_HEADER_SETTINGS = Locator.id("eva-subnav-5")
    D_HEADER_DOWNLOAD = Locator.id("eva-subnav-6")
    D_HEADER_FAQ = Locator.id("eva-subnav-7")
    FILTERS_BLOCK = Locator(By.CSS_SELECTOR, "[class*='catalog-filters_root']")
    FILTERS_BUTTON = Locator(By.CSS_SELECTOR, "[class*='Catalog_filterTitle']")
    FILTERS_RESET_BUTTON = Locator.id("resetCatalogFilters")
    FILTER_MMO_GENRE = Locator.xpath(".//*[contains(text(), 'MMORPG')]")
    FILTERS_TARIFF_CHECKBOX = Locator.xpath(".//*[contains(text(), 'Лайт')]")
    FILTERS_LAUNCHER_CHECKBOX = Locator.xpath(".//*[contains(text(), 'Лаунчер Steam')]")
    FILTERS_SHOW_BUTTON = Locator(By.CSS_SELECTOR, "[class*='catalog-filters_submitBtn']")
    FILTERS_BACK_BUTTON = Locator(By.CSS_SELECTOR, "[class*='back-button_backBtn']")

    dashboard_blocks = {
        "CONTENT_BLOCK": CONTENT_BLOCK,
        "SEARCH_BLOCK": SEARCH_BLOCK,
        "D_HEADER_MAIN": D_HEADER_MAIN,
        "D_HEADER_TASKS": D_HEADER_TASKS,
        "D_HEADER_PLANS": D_HEADER_PLANS,
        "D_HEADER_SETTINGS": D_HEADER_SETTINGS,
        "D_HEADER_DOWNLOAD": D_HEADER_DOWNLOAD,
        "D_HEADER_FAQ": D_HEADER_FAQ,
        "CATALOG_BLOCK": CATALOG_BLOCK,
        "TASKS_CONTENT_BLOCK": TASKS_CONTENT_BLOCK,
        "PLANS_CONTENT_BLOCK": PLANS_CONTENT_BLOCK,
        "SETTINGS_CONTENT_BLOCK": SETTINGS_CONTENT_BLOCK,
        "FAQ_CONTENT_BLOCK": FAQ_CONTENT_BLOCK,
        "DOWNLOAD_CONTENT_BLOCK": DOWNLOAD_CONTENT_BLOCK,
        "DOWNLOAD_MOBILE_BLOCK": DOWNLOAD_MOBILE_BLOCK,
        "DOWNLOAD_TV_BLOCK": DOWNLOAD_TV_BLOCK,
        "FILTERS_BLOCK": FILTERS_BLOCK,
        "FILTERS_TARIFF_CHECKBOX": FILTERS_TARIFF_CHECKBOX,
    }
