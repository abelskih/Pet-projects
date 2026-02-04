import time
from collections.abc import Callable
from typing import Any, Optional, Union

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains, Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from src.configs import vkplay_config
from src.utils.locators import Locator
from src.utils.network_driver import NetworkDriver


class BasePageAbstract:
    def __init__(self, app, url):
        self.app = app
        self.url = url

    def open_page(self, param: Optional[str] = "") -> None:
        self.app.driver.get(self.url + param)
        self.app.driver.implicitly_wait(5)

    def set_browser_window_size(self, width=1366, height=1080):
        self.app.driver.set_window_size(width, height)

    def go_to_url(self, url: str) -> None:
        self.app.driver.get(url)

    def refresh_page(self) -> None:
        self.app.driver.refresh()

    def get_cookie(self, cookie: str) -> str:
        """
        Get user cookie
        :param cookie:
        :return:
        """
        return self.app.driver.get_cookie(cookie)

    def add_cookie(self, cookie: str, value: str, domain: str) -> None:
        self.app.driver.add_cookie({"name": cookie, "value": value, "domain": domain})

    def add_local_cookie(self, key: str, value: str):
        self.app.driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")

    def delete_cookies(self) -> None:
        self.app.driver.delete_all_cookies()

    def get_current_url(self) -> str:
        return self.app.driver.current_url

    def check_element_is_present(
        self,
        element: Locator,
        timeout: Optional[int] = vkplay_config.ELEMENT_PRESENT_TIMEOUT,
        clickable: Optional[bool] = True,
    ) -> Union[WebElement, bool]:
        if clickable:
            try:
                return self.wait_until_clickable(*element, timeout=timeout)
            except TimeoutException:
                return False
        else:
            try:
                return self.wait_until_visible(*element, timeout=timeout)
            except TimeoutException:
                return False

    def check_element_is_not_present(
        self, element: Locator, timeout: Optional[int] = vkplay_config.ELEMENT_PRESENT_TIMEOUT
    ) -> bool:
        try:
            self.wait_until_visible(*element, timeout=timeout)
        except TimeoutException:
            return True
        else:
            return False

    def wait_until_visible(
        self, by: str, value: str, timeout: Optional[int] = vkplay_config.WAIT_TIMEOUT
    ) -> WebElement:
        try:
            wd = self.app.driver
            return WebDriverWait(wd, timeout).until(ec.visibility_of_element_located((by, value)))
        except TimeoutException:
            raise TimeoutException(f"Can't find element on page. \nElement: {value}\nBy: {by}")

    def wait_until_multiple_visible(
        self, by: str, value: str, timeout: Optional[int] = vkplay_config.WAIT_TIMEOUT
    ) -> list:
        wd = self.app.driver
        return WebDriverWait(wd, timeout).until(ec.visibility_of_all_elements_located((by, value)))

    def wait_until_not_visible(self, by: str, value: str, timeout: Optional[int] = vkplay_config.WAIT_TIMEOUT) -> bool:
        wd = self.app.driver
        return bool(WebDriverWait(wd, timeout).until_not(ec.visibility_of_element_located((by, value))))

    def wait_until_clickable(
        self, by: str, value: str, timeout: Optional[int] = vkplay_config.WAIT_TIMEOUT
    ) -> WebElement:
        wd = self.app.driver
        return WebDriverWait(wd, timeout).until(ec.element_to_be_clickable((by, value)))

    def wait_until_not_clickable(
        self, by: str, value: str, timeout: Optional[int] = vkplay_config.WAIT_TIMEOUT
    ) -> bool:
        wd = self.app.driver
        return bool(WebDriverWait(wd, timeout).until_not(ec.element_to_be_clickable((by, value))))

    def wait_until_multiple_present(
        self, by: str, value: str, timeout: Optional[int] = vkplay_config.WAIT_TIMEOUT
    ) -> list:
        wd = self.app.driver
        return WebDriverWait(wd, timeout).until(ec.presence_of_all_elements_located((by, value)))

    def wait_until_frame_to_be_available_and_switch_to_it(
        self, by: str, value: str, timeout: Optional[int] = vkplay_config.WAIT_TIMEOUT
    ) -> bool:
        """
        Wait until iframe be available to interaction and switch to it
        :param by:
        :param value:
        :param timeout:
        :return:
        """
        wd = self.app.driver
        return WebDriverWait(wd, timeout).until(ec.frame_to_be_available_and_switch_to_it((by, value)))

    def wait_until_text(
        self,
        by: str,
        value: str,
        text: str,
        timeout: Optional[int] = vkplay_config.WAIT_TIMEOUT,
    ) -> bool:
        wd = self.app.driver
        return WebDriverWait(wd, timeout).until(ec.text_to_be_present_in_element((by, value), text))

    def wait_until_count(self, element: Locator, count: int, timeout=vkplay_config.WAIT_TIMEOUT) -> None:
        """wait until the elements are displayed in the required quantity"""
        end_time = time.time() + timeout
        while time.time() < end_time:
            if len(self.wait_until_multiple_visible(*element)) == count:
                break
        else:
            raise TimeoutException("The number of elements does not match the required number")

    def wait_until_current_url_changes(
        self, expected_url: str, timeout: Optional[int] = vkplay_config.WAIT_TIMEOUT
    ) -> None:
        """
        Wait for url change in browser from current url to expected url

        Args:
            timeout (Optional[int], optional): _description_. Defaults to vkplay_config.WAIT_TIMEOUT.
        """
        wd = self.app.driver
        current_url = self.get_current_url()
        if WebDriverWait(wd, timeout).until(ec.url_changes(current_url)):
            return self.is_correct_link(expected_url)

        raise TimeoutException("Url is not changed")

    @staticmethod
    def wait_request_finished(
        request: Callable,
        value: Any,
        message: str = "Data was not saved",
        timeout: int = vkplay_config.WAIT_TIMEOUT,
        **params: Any,
    ) -> Optional[bool]:
        end_time = time.time() + timeout
        while time.time() < end_time:
            if request(**params) == value:
                return True
        else:
            raise TimeoutException(message)

    def get_value(self, locator: str) -> str:
        wd = self.app.driver
        return wd.execute_script(f'return document.querySelector("{locator}").value')

    def count_elements(self, locator: Locator, count) -> int:
        self.wait_until_count(locator, count)
        return len(self.wait_until_multiple_visible(*locator))

    def move_to_element(self, element: WebElement) -> None:
        wd = self.app.driver
        ActionChains(wd).move_to_element(element).perform()

    def disable_smooth_scroll(self, element: WebElement) -> None:
        wd = self.app.driver
        wd.execute_script("arguments[0].style.scrollBehavior = 'auto';", element)

    def move_to_element_coordinates_and_click(self, element: WebElement, x: int, y: int) -> None:
        wd = self.app.driver
        ActionChains(wd).move_to_element_with_offset(element, x, y).click().perform()

    def scroll_to_element(self, element: WebElement) -> None:
        wd = self.app.driver

        # Проверяем, что элемент существует и не None
        if not element:
            raise ValueError("Element is None")

        # Проверяем, что элемент все еще присутствует в DOM
        is_present = wd.execute_script("return document.contains(arguments[0]);", element)
        if not is_present:
            raise ValueError("Element is not present in DOM")

        # Проверяем, что элемент является стандартным DOM-элементом
        is_valid = wd.execute_script(
            """
            return arguments[0] instanceof Element &&
                   typeof arguments[0].scrollIntoView === 'function';
        """,
            element,
        )

        if is_valid:
            # Используем основной метод прокрутки
            wd.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        else:
            # Используем альтернативный метод прокрутки
            try:
                location = element.location_once_scrolled_into_view
                wd.execute_script(f"window.scrollTo(0, {location['y']});")
            except Exception:
                # Если и альтернативный метод не работает, используем ActionChains
                actions = ActionChains(wd)
                actions.move_to_element(element).perform()

    def change_tab(self, window_number: int) -> None:
        wd = self.app.driver
        wd.switch_to.window(wd.window_handles[window_number])

    def close_active_tab(self) -> None:
        wd = self.app.driver
        wd.close()

    def get_count_tab(self) -> int:
        wd = self.app.driver
        return len(wd.window_handles)

    def is_correct_link(self, substring_url) -> bool:
        current_url = self.app.driver.current_url
        return substring_url in current_url

    def is_redirected(self, substring_url: str):
        current_url = self.app.driver.current_url
        return substring_url in current_url

    # TODO: used as a workaround of mising typings in app class
    # (could not be done correctly in the current project configuration)
    def get_driver(self) -> Chrome:
        return self.app.driver

    def get_network(self) -> NetworkDriver:
        return self.app.network

    def click_button(self, by: str, value: str) -> None:
        """
        Wait until button will be clickable and click to it
        :param by:
        :param value:
        :return:
        """
        self.wait_until_clickable(by, value).click()

    def try_to_click_button(self, by: str, value: str, max_attempts: int = 3):
        """
        Отличается от функции click_button тем, что проверяет наличие кнопки несколько раз.
        Помогает в редких случаях, когда возникает ошибка StaleElementReferenceException.

        Args:
            by (str): locator by
            value (str): locator value
            max_attempts (int, optional) Defaults to 3.
        """
        attempts = 0
        while attempts < 3:
            try:
                self.wait_until_clickable(by, value).click()
                break
            except StaleElementReferenceException:
                attempts += 1
                if attempts == max_attempts:
                    raise

    def send_input_value(self, by: str, value: str, text: str) -> None:
        """
        Wait until input will be clickable ant send value to it
        :param by:
        :param value:
        :param text:
        :return:
        """
        self.wait_until_clickable(by, value).send_keys(text)

    def check_is_url_in_element_href(self, element: WebElement, expected_url: str) -> bool:
        """
        Check that exected url is inside element's href

        Args:
          element (WebElement):
          expected_url (str): Expected url in href value
        """
        return expected_url in element.get_attribute("href")

    def clear_auth_data_in_browser(self):
        """
        Delete cookies, local storage and session data.
        Will be useful for cleaning up after authorization
        """
        self.delete_cookies()
        self.get_driver().execute_script("localStorage.clear()")
        self.get_driver().execute_script("sessionStorage.clear()")
