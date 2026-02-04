import re

import pytest

from src.api import cloud_api
from src.components.header.header_component import HeaderComponent
from src.components.plan_selector.plan_selector_component import PlanSelectorComponent
from src.configs import vkplay_config
from src.pages.account.account_page import AccountPage
from src.pages.base_page_vkplay import BasePageVKPlay
from src.pages.cloud.dashboard_page import DashboardPage
from src.utils.common import convert_price_text_to_num, get_url_without_protocol


@pytest.mark.cloud()
class TestCloudDashboard:
    def _get_api_plan_by_name(self, name: str, api_plans: list) -> dict:
        for plan in api_plans:
            if name.lower() == plan["name"].lower():
                return plan
        raise AssertionError(f"Plan name '{name}' not found in API response")

    def _minutes_text_to_minutes(self, minutes_text: str) -> int:
        match = re.search(r"\d+", minutes_text)
        assert match, f"No minutes value in UI text: '{minutes_text}'"
        return int(match.group()) * 60

    def _get_quests_without_initial(self, user_quests: list) -> list:
        if user_quests and user_quests[0].get("quest_type") == "initial":
            return user_quests[1:]
        return user_quests

    def _compare_catalog_with_api(self, cards_data: list, api_games: list) -> None:
        assert len(cards_data) > 0, "Catalog is empty"
        for idx, card in enumerate(cards_data):
            api_game = api_games[idx]
            assert card["name"] == api_game["name"]
            assert card["genre_descr"] == api_game["genre_descr"]
            assert card["age_limit"] == api_game["age_limit"]
            jpg = self.page.get_filename_from_url(api_game["picture"])
            assert jpg in card["picture"]

    def get_url_for_tests(self, app, request) -> str:
        url = app.url["cloud_link"] + vkplay_config.CloudLinks.Pages.DASHBOARD
        if request.config.getoption("--url") == "cloud_predprod":
            predprod_user = request.config.getoption("--cloud_user")
            predprod_pass = request.config.getoption("--cloud_pass")
            if not predprod_user and not predprod_pass:
                pytest.fail("Predprod run requires both --cloud_user and --cloud_pass")
                return

            return f"http://{predprod_user}:{predprod_pass}@{get_url_without_protocol(url)}"

        return url

    @pytest.fixture(autouse=True)
    def setup(self, app, request):
        self.page_url = self.get_url_for_tests(app, request)
        self.assert_page_url = app.url["cloud_link"] + vkplay_config.CloudLinks.Pages.DASHBOARD
        self.test_user = vkplay_config.USER_DATA["user_email_2"]

        self.page = DashboardPage(app, self.page_url)
        self.account_page = AccountPage(app, self.page_url)
        self.base_page = BasePageVKPlay(app, self.page_url)
        self.plan_selector = PlanSelectorComponent(app, self.page_url)

        self.page.open_page()
        self.page.add_local_cookie("rent_games_catalog_hint_show", "true")

    @pytest.fixture(autouse=False)
    def use_cookie_auth(self):
        self.base_page.update_auth_cookies(self.test_user["login"], self.test_user["password"])
        self.account_page.fast_login(self.test_user["login"], self.test_user["password"])
        yield
        self.page.clear_auth_data_in_browser()

    @pytest.fixture(autouse=False)
    def use_logpass_auth(self, app):
        self.base_page.update_auth_cookies(self.test_user["login"], self.test_user["password"])
        self.header_page = HeaderComponent(app, self.page_url)
        self.header_page.click_navigation_button("auth")
        self.account_page.login_by_email_or_phone(
            self.test_user["login"],
            self.test_user["password"],
        )
        self.account_page.wait_until_spinner_is_not_visible()
        assert self.account_page.check_user_authenticated()
        yield
        self.page.clear_auth_data_in_browser()

    def test__613886_613882_613884__catalog_content_for_unauthorized_user(self):
        assert self.page.is_dashboard_block_visible("CONTENT_BLOCK")
        assert self.page.is_dashboard_block_visible("SEARCH_BLOCK")
        assert self.page.check_dashboard_header_is_not_visible()

        cards_data = self.page.get_catalog_cards_data()
        api_games = cloud_api.get_games()
        self._compare_catalog_with_api(cards_data, api_games)

    @pytest.mark.parametrize("text", ["Atomic Heart", "Warface", "Genshin Impact"])
    def test__613885__search_field(self, text):
        self.page.search_game_by_name(text)
        assert self.page.check_search_result(text)

    def test__613925__negative_search_not_exist(self):
        self.page.search_game_by_name("asdasdasdasd")
        assert self.page.check_is_empty_search_result_shown()

    @pytest.mark.usefixtures("use_logpass_auth")
    def test__613883__catalog_for_authorized_user(self):
        assert self.page.is_correct_link(self.assert_page_url)
        assert len(self.page.get_catalog_cards_data()) > 0

    @pytest.mark.usefixtures("use_cookie_auth")
    def test__614038__dashboard_header_content(self):
        assert self.page.check_dashboard_header_is_visible()
        self.page.click_dashboard_button("D_HEADER_MAIN")
        assert self.page.is_correct_link(self.assert_page_url)
        assert self.page.is_dashboard_block_visible("CATALOG_BLOCK")

    @pytest.mark.usefixtures("use_cookie_auth")
    def test__614150__dashboard_tasks_page(self, app):
        self.page.click_dashboard_button("D_HEADER_TASKS")
        assert self.page.is_correct_link(app.url["cloud_link"] + vkplay_config.CloudLinks.Pages.TASKS)
        assert self.page.is_dashboard_block_visible("TASKS_CONTENT_BLOCK")

        cookie = self.page.create_header_cookie_for_cloud_request(self.test_user["login"])
        api_user_quests = cloud_api.get_user_quests(cookie)
        api_user_quests = self._get_quests_without_initial(api_user_quests)

        cards_data = self.page.get_task_cards_data()
        for num, card in enumerate(cards_data):
            api_quest_name = api_user_quests[num]["title"].replace("&nbsp;", " ")
            assert card["name"] == api_quest_name
            assert api_user_quests[num]["image_url"] in card["bg_picture"]

    @pytest.mark.usefixtures("use_cookie_auth")
    def test__614150__dashboard_plans_page(self, app):
        self.page.click_dashboard_button("D_HEADER_PLANS")
        assert self.page.is_correct_link(app.url["cloud_link"] + vkplay_config.CloudLinks.Pages.PLANS)
        assert self.page.is_dashboard_block_visible("PLANS_CONTENT_BLOCK")

        api_plans = cloud_api.get_plans()

        hour_plans = self.plan_selector.get_hour_plans_ui_data()
        for ui_plan in hour_plans:
            api_plan = self._get_api_plan_by_name(ui_plan["name"], api_plans)
            api_price = convert_price_text_to_num(api_plan["price"])
            if api_plan.get("discount"):
                api_discounted_price = convert_price_text_to_num(api_plan["discount"]["price"])
                assert ui_plan["price"] == api_discounted_price
                assert ui_plan["old_price"] == api_price
            else:
                assert ui_plan["price"] == api_price
                assert ui_plan["old_price"] is None

            ui_minutes = self._minutes_text_to_minutes(ui_plan["minutes_text"])
            assert ui_minutes == int(api_plan["included_minutes"])

        month_plans = self.plan_selector.get_month_plans_ui_data()
        for ui_plan in month_plans:
            api_plan = self._get_api_plan_by_name(ui_plan["name"], api_plans)
            api_price = convert_price_text_to_num(api_plan["price"])
            if api_plan.get("discount"):
                api_discounted_price = convert_price_text_to_num(api_plan["discount"]["price"])
                assert ui_plan["price"] == api_discounted_price
                assert ui_plan["old_price"] == api_price
            else:
                assert ui_plan["price"] == api_price
                assert ui_plan["old_price"] is None

    @pytest.mark.usefixtures("use_cookie_auth")
    def test__614041__dashboard_settings_page(self, app):
        self.page.click_dashboard_button("D_HEADER_SETTINGS")
        assert self.page.is_correct_link(app.url["cloud_link"] + vkplay_config.CloudLinks.Pages.SETTINGS)
        assert self.page.is_dashboard_block_visible("SETTINGS_CONTENT_BLOCK")

    @pytest.mark.usefixtures("use_cookie_auth")
    def test__614042__dashboard_download_page(self, app):
        self.page.click_dashboard_button("D_HEADER_DOWNLOAD")
        assert self.page.is_correct_link(app.url["cloud_link"] + vkplay_config.CloudLinks.Pages.DOWNLOAD)
        assert self.page.is_dashboard_block_visible("DOWNLOAD_CONTENT_BLOCK")

        mobile_buttons = self.page.get_buttons_from_block("DOWNLOAD_MOBILE_BLOCK")
        assert self.page.check_is_url_in_element_href(mobile_buttons[0], vkplay_config.GOOGLE_PLAY_LINK)
        assert self.page.check_is_url_in_element_href(mobile_buttons[1], vkplay_config.CloudLinks.Apk.MOBILE_APK)

        tv_buttons = self.page.get_buttons_from_block("DOWNLOAD_TV_BLOCK")
        assert self.page.check_is_url_in_element_href(tv_buttons[0], vkplay_config.GOOGLE_PLAY_LINK)
        assert self.page.check_is_url_in_element_href(tv_buttons[1], vkplay_config.RUSTORE_LINK)
        assert self.page.check_is_url_in_element_href(tv_buttons[2], vkplay_config.CloudLinks.Apk.TV_APK)

    @pytest.mark.usefixtures("use_cookie_auth")
    def test__614043__dashboard_faq_page(self, app):
        self.page.click_dashboard_button("D_HEADER_FAQ")
        assert self.page.is_correct_link(app.url["cloud_link"] + vkplay_config.CloudLinks.Pages.FAQ)
        assert self.page.is_dashboard_block_visible("FAQ_CONTENT_BLOCK")

    def test__451576__filter_block_is_opened(self):
        self.page.open_filter_block()
        assert self.page.is_dashboard_block_visible("FILTERS_BLOCK")

    def test__451573__filters_reset_by_button(self):
        self.page.open_filter_block()
        self.page.select_mmo_genre()
        self.page.reset_all_filters()
        self.page.close_filter_block()

        cards_data = self.page.get_catalog_cards_data()
        api_games = cloud_api.get_games()
        self._compare_catalog_with_api(cards_data, api_games)

    def test__451589__catalog_changes_when_some_filter_selected(self):
        self.page.open_filter_block()
        self.page.select_mmo_genre()
        self.page.click_show_button()

        cards_data = self.page.get_catalog_cards_data()
        api_games = cloud_api.get_games(1, 24, "mmo", None)
        self._compare_catalog_with_api(cards_data, api_games)

    def test__451572__catalog_changes_by_several_options(self):
        self.page.open_filter_block()
        self.page.select_mmo_genre()
        self.page.select_tariff("FILTERS_TARIFF_CHECKBOX")
        self.page.click_show_button()

        cards_data = self.page.get_catalog_cards_data()
        api_games = cloud_api.get_games(1, 24, "mmo", "mygames")
        self._compare_catalog_with_api(cards_data, api_games)
