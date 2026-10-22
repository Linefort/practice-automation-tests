import allure
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        StaleElementReferenceException, TimeoutException)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    url = ""
    HEADING = (By.TAG_NAME, "h1")
    SUCCESS_MESSAGE = (By.XPATH, "//*[contains(normalize-space(text()), 'Thank you for your response')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Открыть страницу")
    def open(self):
        self.driver.get(self.url)
        # при eager-загрузке get() возвращается до выполнения скриптов сайта - дожидаемся готовности
        self.wait_until(lambda: self.driver.execute_script("return document.readyState") == "complete", 15)
        self.wait_page_ready()

    def wait_page_ready(self):
        # страница переопределяет метод, если её скриптам нужен свой сигнал готовности
        pass

    @property
    def title(self):
        return self.driver.title

    @property
    def heading(self):
        return self.find_visible(self.HEADING).text.strip()

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_until(self, condition, timeout=10):
        # возвращает False вместо исключения, чтобы в тестах писать обычный assert
        # poll_frequency=0.2 - опрос страницы в 2.5 раза чаще стандартного
        wait = WebDriverWait(self.driver, timeout, poll_frequency=0.2,
                             ignored_exceptions=[StaleElementReferenceException])
        try:
            wait.until(lambda d: condition())
            return True
        except TimeoutException:
            return False

    # на страницах есть скрытые копии окон и форм, поэтому смотрим на все найденные элементы
    def is_visible(self, locator):
        for element in self.driver.find_elements(*locator):
            try:
                if element.is_displayed():
                    return True
            except StaleElementReferenceException:
                # элемент пропал со страницы, пока мы его проверяли (например, окно закрылось)
                continue
        return False

    def wait_visible(self, locator, timeout=10):
        return self.wait_until(lambda: self.is_visible(locator), timeout)

    def wait_invisible(self, locator, timeout=10):
        return self.wait_until(lambda: not self.is_visible(locator), timeout)

    def stays_hidden(self, locator, seconds):
        # ждём указанное время: если элемент так и не появился, возвращаем True
        return not self.wait_until(lambda: self.is_visible(locator), seconds)

    def stays_visible(self, locator, seconds):
        # ждём указанное время: если элемент всё это время был виден, возвращаем True
        return not self.wait_until(lambda: not self.is_visible(locator), seconds)

    def get_text(self, locator):
        return self.find_visible(locator).text.strip()

    def get_value(self, locator):
        return self.find(locator).get_attribute("value") or ""

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator, text):
        element = self.find_visible(locator)
        element.clear()
        element.send_keys(text)

    def press_key(self, key):
        ActionChains(self.driver).send_keys(key).perform()

    def is_reachable(self, locator):
        # true, если в центре элемента лежит он сам, а не окно поверх него
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        return self.driver.execute_script(
            "const r = arguments[0].getBoundingClientRect();"
            "const top = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2);"
            "return arguments[0].contains(top);",
            element)

    def is_success_visible(self):
        return self.is_visible(self.SUCCESS_MESSAGE)

    def wait_success_visible(self, timeout=10):
        return self.wait_visible(self.SUCCESS_MESSAGE, timeout)
