from selenium.webdriver.common.by import By


class Locator:
    def __init__(self, by: str, value: str):
        self._storage = [by, value]

    @property
    def by(self) -> str:
        return self._storage[0]

    @property
    def value(self) -> str:
        return self._storage[1]

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self) -> str:
        if self.n < len(self._storage):
            self.n += 1
            return self._storage[self.n - 1]
        else:
            raise StopIteration

    @staticmethod
    def css(value: str):
        return Locator(By.CSS_SELECTOR, value)

    @staticmethod
    def data_id(value: str):
        return Locator(By.CSS_SELECTOR, f'[data-id="{value}"]')

    @staticmethod
    def data_test(value: str):
        return Locator(By.CSS_SELECTOR, f'[data-test="{value}"]')

    @staticmethod
    def data_testid(value: str):
        return Locator(By.CSS_SELECTOR, f'[data-testid="{value}"]')

    @staticmethod
    def data_test_id(value: str):
        return Locator(By.CSS_SELECTOR, f'[data-test-id="{value}"]')

    @staticmethod
    def data_tooltip_id(value: str):
        return Locator(By.CSS_SELECTOR, f'[data-tooltip-id="{value}"]')

    @staticmethod
    def id(value: str):
        return Locator(By.ID, value)

    @staticmethod
    def xpath(value: str):
        return Locator(By.XPATH, value)

    @staticmethod
    def class_starts_with(value: str):
        """Only for one class. For more use Locator.css()"""
        return Locator(By.CSS_SELECTOR, f'[class^="{value}"]')

    @staticmethod
    def name(value: str):
        return Locator(By.NAME, value)
