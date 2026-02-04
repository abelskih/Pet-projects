import platform

import allure
import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from src.configs import vkplay_config
from src.utils.network_driver import NetworkDriver

URL_MAP = {
    "cloud": {
        "domain": "vkplay_prod",
        "links": {
            "account_link": "https://account.vkplay.ru/",
            "cloud_link": "https://cloud.vkplay.ru/",
            "cloud_static_link": "https://static.gc.vkplay.ru/",
            "cloud_cdn_link": "https://vkplaycloud.mrgcdn.ru/",
        },
    }
}


class Application:
    def __init__(self, browser: str, launch: str, url: str):
        self.launch = launch
        self.browser = browser
        self.url = url
        self.driver = None
        self.run_browser(browser, launch)
        self.network = NetworkDriver(self.driver)

    def run_browser(self, browser: str, launch: str) -> None:
        if browser != "chrome":
            raise Exception("Only chrome is supported in minimal cloud setup")
        if launch != "local":
            raise Exception("Only local launch is supported in minimal cloud setup")
        self._launch_local()

    def _launch_local(self) -> None:
        options = Options()
        options.add_argument("acceptSslCerts=True")
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        self.driver = Chrome(options=options)
        self.driver.maximize_window()

    def make_screen(self):
        return self.driver.get_screenshot_as_png()

    def destroy(self):
        self.driver.quit()


@pytest.fixture(scope="session")
def app(request):
    browser = request.config.getoption("--browser")
    launch = request.config.getoption("--launch")
    url_key = request.config.getoption("--url")

    if url_key not in URL_MAP:
        raise Exception(f"Unknown url key: {url_key}. Available: {', '.join(URL_MAP)}")

    url_data = URL_MAP[url_key]
    vkplay_config.domain = url_data["domain"]

    application = Application(browser=browser, url=url_data["links"], launch=launch)
    yield application
    application.destroy()


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--url", action="store", default="cloud")
    parser.addoption("--launch", action="store", default="local")
    parser.addoption("--cloud_user", action="store", default=None)
    parser.addoption("--cloud_pass", action="store", default=None)


def pytest_configure(config):
    config.addinivalue_line("markers", "vkplay: vkplay tests")
    config.addinivalue_line("markers", "cloud: cloudgaming tests")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()
    if result.when == "call":
        feature_request = item.funcargs["request"]
        driver = feature_request.getfixturevalue("app")
        xfail = hasattr(result, "wasxfail")
        if platform.system() != "Windows" or item.config.option.launch == "remote":
            if result.failed and not xfail:
                allure.attach(
                    name="Screenshot",
                    body=driver.make_screen(),
                    attachment_type=allure.attachment_type.PNG,
                )
