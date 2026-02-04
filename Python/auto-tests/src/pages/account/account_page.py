import allure
from src.pages.account.locators import AccountPageLocators
from src.pages.base_page_vkplay import BasePageVKPlay

socials = {
    "mail.ru": AccountPageLocators.MAIL_RU_AUTH_BUTTON,
    "ok": AccountPageLocators.OK_AUTH_BUTTON,
}


class AccountPage(BasePageVKPlay):
    @allure.step("Осуществляем быстрый логин через куки")
    def fast_login(self, login: str, password: str, wait_for_spinner: bool = False) -> None:
        n_attempts = 3
        for _ in range(n_attempts):
            self.add_auth_cookies_to_browser(login, password)
            self.refresh_page()
            if wait_for_spinner:
                self.wait_until_spinner_is_not_visible()
            if self.check_authenticated_avatar(2):
                break
            self.update_auth_cookies(login, password)
        else:
            raise Exception("Unable to authorize")

    def login_by_email_or_phone(self, login: str, password: str) -> None:
        """
        Login by email/phone
        :param login:
        :param password:
        :return:
        """
        self.wait_until_visible(*AccountPageLocators.LOGIN_FIELD)
        self.send_input_value(*AccountPageLocators.LOGIN_FIELD, login)
        self.click_social_login_button()
        self.wait_until_visible(*AccountPageLocators.PASSWORD_FIELD)
        self.send_input_value(*AccountPageLocators.PASSWORD_FIELD, password)
        self.click_social_login_button()

    def wait_until_spinner_is_not_visible(self) -> None:
        self.wait_until_not_visible(*AccountPageLocators.SPINNER)

    def is_login_input_present(self) -> bool:
        return bool(self.check_element_is_present(AccountPageLocators.LOGIN_FIELD, timeout=2))

    def is_password_input_present(self) -> bool:
        return bool(self.check_element_is_present(AccountPageLocators.PASSWORD_FIELD, timeout=2))

    def click_social_login_button(self) -> None:
        """
        Click submit button
        """
        self.click_button(*AccountPageLocators.SUBMIT_BUTTON)

    def click_social_auth_button(self, social_name: str) -> None:
        self.click_button(*socials[social_name])

    def wait_until_login_field_visible(self):
        self.wait_until_visible(*AccountPageLocators.LOGIN_FIELD)
