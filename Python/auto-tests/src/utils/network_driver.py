import base64

from selenium.webdriver import Chrome

# TODO: add class description


# === NOTE ===
# The following code is based on Chrome DevTools Protocol.
# Selenium does not provide any common mechanics to intercept request. That is why CDP used.
# All functions defined below could work only on Chrome WebDriver. Be careful.
class NetworkDriver:
    def __init__(self, web_driver: Chrome):
        self.web_driver = web_driver
        self.is_enabled = False
        self.extra_headers = {}

    def enable(self) -> None:
        """
        Enables Network control through CDP
        :return:
        """
        if self.is_enabled:
            return

        self.web_driver.execute_cdp_cmd("Network.enable", {})
        self.is_enabled = True

    def disable(self) -> None:
        """
        Disables Network control through CDP
        :return:
        """
        if not self.is_enabled:
            return

        self.reset()
        self.web_driver.execute_cdp_cmd("Network.disable", {})
        self.is_enabled = False

    def set_extra_request_headers(self, headers) -> None:
        """
        Adds extra request headers to all requests
        :param headers:
        :return:
        """
        self.__validate_is_enabled()

        self.extra_headers = headers

        self.web_driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": self.extra_headers})

    def clear_extra_request_headers(self) -> None:
        """
        Clear extra request headers
        :return:
        """
        headers = {}
        for key in self.extra_headers.keys():
            headers[key] = ""

        self.extra_headers = headers
        self.web_driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": headers})

    def reset(self) -> None:
        """
        Resets headers, cache and cookies
        :return:
        """
        self.clear_extra_request_headers()
        self.web_driver.execute_cdp_cmd("Network.clearBrowserCache", {})
        self.web_driver.execute_cdp_cmd("Network.clearBrowserCookies", {})

    def use_basic_authorization(self, credentials: str) -> None:
        """
        Pass basic auth authorization
        :param credentials: user credentials in ```{username}:{password}``` format
        :return:
        """
        self.__validate_is_enabled()

        # Encrypt Basic Auth credentials using base64 algorithm
        encrypted_credentials = base64.b64encode(credentials.encode()).decode()

        # Create Basic Auth headers
        headers = {"authorization": "Basic " + encrypted_credentials}

        # Attach authorization headers
        self.set_extra_request_headers(headers)

    def __validate_is_enabled(self) -> None:
        """
        Validate condition of network
        :return:
        """
        if not self.is_enabled:
            raise Exception("Network is disabled. Probably you forgot to enable it")
