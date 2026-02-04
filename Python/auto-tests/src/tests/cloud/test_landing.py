import re

import pytest

from src.api import cloud_api
from src.components.plan_selector.plan_selector_component import PlanSelectorComponent
from src.configs import vkplay_config
from src.pages.cloud.landing_page import LandingPage
from src.utils.common import convert_price_text_to_num, get_url_without_protocol


@pytest.mark.cloud()
class TestCloudLanding:
    def _get_api_plan_by_name(self, name: str, api_plans: list) -> dict:
        for plan in api_plans:
            if name.lower() == plan["name"].lower():
                return plan
        raise AssertionError(f"Plan name '{name}' not found in API response")

    def _minutes_text_to_minutes(self, minutes_text: str) -> int:
        match = re.search(r"\d+", minutes_text)
        assert match, f"No minutes value in UI text: '{minutes_text}'"
        return int(match.group()) * 60

    def get_url_for_tests(self, app, request) -> str:
        url = app.url["cloud_link"]
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
        self.page = LandingPage(app, self.page_url)
        self.plans_component = PlanSelectorComponent(app, self.page_url)

    def test_check_landing_blocks_shown(self):
        self.page.open_page()
        assert self.page.check_landing_blocks_are_shown()

    @pytest.mark.parametrize(
        ("block_name", "content_block_name"),
        [
            ("ABOUT_BLOCK", "ABOUT_BLOCK_IMGS"),
            ("FEATURES_BLOCK", "FEATURES_ITEMS_IMG"),
            ("VIDEO_COMPARSION_BLOCK", "VIDEO_COMPARSION_VIDEO"),
            ("ANY_MACHINE_BLOCK", "ANY_MACHINE_BG"),
        ],
    )
    def test_blocks_content_is_loaded(self, block_name, content_block_name):
        self.page.open_page()
        assert self.page.check_content_is_loaded(block_name, content_block_name)

    def test__568744__any_machine_direct_download_buttons(self, app):
        self.page.open_page()
        hrefs = self.page.check_direct_download_buttons_in_block(block_name="ANY_MACHINE_BLOCK")
        assert app.url["cloud_static_link"] in hrefs[0]
        assert (app.url["cloud_static_link"] + vkplay_config.CloudLinks.Static.MAC) in hrefs[1]

    @pytest.mark.parametrize(
        ("button_number", "expected_apk_url"),
        [
            (0, vkplay_config.CloudLinks.Apk.MOBILE_APK),
            (1, vkplay_config.CloudLinks.Apk.TV_APK),
        ],
    )
    def test__568744__any_machine_android_download_buttons(self, button_number, expected_apk_url):
        self.page.open_page()
        popup_data = self.page.check_popup_download_buttons_click("ANY_MACHINE_BLOCK", button_number)
        assert expected_apk_url in popup_data["direct"]
        assert vkplay_config.GOOGLE_PLAY_LINK in popup_data["stores"][0]
        if len(popup_data["stores"]) > 1:
            assert vkplay_config.RUSTORE_LINK in popup_data["stores"][1]

    def test__568769__click_view_games_button(self, app):
        self.page.open_page()
        self.page.click_button_on_landing("GAMES_BLOCK_PLAY_BUTTON")
        assert self.page.is_correct_link(app.url["cloud_link"] + vkplay_config.CloudLinks.Pages.DASHBOARD)

    def test__568722__plans_block(self):
        self.page.open_page()
        api_plans = cloud_api.get_plans()

        hour_plans = self.plans_component.get_hour_plans_ui_data()
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

        month_plans = self.plans_component.get_month_plans_ui_data()
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

    @pytest.mark.parametrize("card_number", [0, 1])
    def test_plan_buy_buttons(self, app, card_number):
        self.page.open_page()
        self.plans_component.click_month_plan_button(card_number)
        assert self.page.is_correct_link(app.url["account_link"])

    @pytest.mark.parametrize(
        "button_name",
        [
            "MAIN_BLOCK_PLAY_BUTTON",
            "ANY_MACHINE_BLOCK_PLAY_BUTTON",
            "LAUNCH_BLOCK_PLAY_BUTTON",
        ],
    )
    def test_play_buttons(self, app, button_name):
        self.page.open_page()
        self.page.click_button_on_landing(button_name)
        assert self.page.is_correct_link(app.url["account_link"])

    def test__568781__plans_play_button(self, app):
        self.page.open_page()
        self.plans_component.switch_plans_to_hours_tab()
        self.page.click_button_on_landing("PLANS_BLOCK_PLAY_BUTTON")
        assert self.page.is_correct_link(app.url["account_link"])
