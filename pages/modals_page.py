import allure
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.popup_page import CLOSE, CONTENT, TITLE, popup_xpath

SIMPLE_XPATH = popup_xpath("Simple Modal")
FORM_XPATH = popup_xpath("Modal Containing A Form")


class ModalsPage(BasePage):
    url = "https://practice-automation.com/modals/"

    SIMPLE_BUTTON = (By.XPATH, "//*[@id='simple_modal' or "
                               "((self::button or self::a) and normalize-space()='Simple Modal')]")
    FORM_BUTTON = (By.XPATH, "//*[@id='form_modal' or "
                             "((self::button or self::a) and normalize-space()='Form Modal')]")

    SIMPLE = (By.XPATH, SIMPLE_XPATH)
    SIMPLE_TITLE = (By.XPATH, SIMPLE_XPATH + TITLE)
    SIMPLE_CONTENT = (By.XPATH, SIMPLE_XPATH + CONTENT)
    SIMPLE_CLOSE = (By.XPATH, SIMPLE_XPATH + CLOSE)

    FORM = (By.XPATH, FORM_XPATH)
    FORM_TITLE = (By.XPATH, FORM_XPATH + TITLE)
    FORM_CONTENT = (By.XPATH, FORM_XPATH + CONTENT)
    FORM_CLOSE = (By.XPATH, FORM_XPATH + CLOSE)
    FORM_SUBMIT = (By.XPATH, FORM_XPATH + "//button[normalize-space()='Submit']")
    FORM_SUCCESS = (By.XPATH, FORM_XPATH + "//*[contains(normalize-space(text()), 'Thank you for your response')]")

    def wait_page_ready(self):
        # Popup Maker создаёт оверлеи при инициализации - сигнал, что скрипты окон готовы
        self.wait_until(lambda: self.driver.execute_script(
            "return document.querySelectorAll('.pum-overlay').length > 0"), 10)

    def is_simple_button_visible(self):
        return self.is_visible(self.SIMPLE_BUTTON)

    def is_form_button_visible(self):
        return self.is_visible(self.FORM_BUTTON)

    @allure.step("Нажать кнопку Simple Modal")
    def open_simple_modal(self):
        self.click(self.SIMPLE_BUTTON)

    @allure.step("Нажать кнопку Form Modal")
    def open_form_modal(self):
        self.click(self.FORM_BUTTON)

    def is_simple_modal_visible(self):
        return self.is_visible(self.SIMPLE)

    def is_form_modal_visible(self):
        return self.is_visible(self.FORM)

    def wait_simple_modal_opened(self):
        return self.wait_visible(self.SIMPLE)

    def wait_simple_modal_closed(self):
        return self.wait_invisible(self.SIMPLE)

    @allure.step("Подождать {seconds} сек и проверить, что Simple Modal осталась открытой")
    def simple_modal_stays_open(self, seconds):
        return self.stays_visible(self.SIMPLE, seconds)

    def wait_form_modal_opened(self):
        return self.wait_visible(self.FORM)

    def wait_form_modal_closed(self):
        return self.wait_invisible(self.FORM)

    def simple_modal_title(self):
        return self.get_text(self.SIMPLE_TITLE)

    def simple_modal_text(self):
        return self.get_text(self.SIMPLE_CONTENT)

    def form_modal_title(self):
        return self.get_text(self.FORM_TITLE)

    def form_modal_text(self):
        return self.get_text(self.FORM_CONTENT)

    @allure.step("Закрыть Simple Modal кнопкой ×")
    def close_simple_modal(self):
        self.click(self.SIMPLE_CLOSE)

    @allure.step("Закрыть Form Modal кнопкой ×")
    def close_form_modal(self):
        self.click(self.FORM_CLOSE)

    def find_form_field(self, label_text):
        # у полей id генерируются автоматически, поэтому ищем по тексту label
        label = self.driver.find_element(
            By.XPATH, f"{FORM_XPATH}//label[starts-with(normalize-space(), '{label_text}')]")
        field_id = label.get_attribute("for")
        if field_id:
            return self.driver.find_element(By.ID, field_id)
        return label.find_element(By.XPATH, ".//input | .//textarea")

    def has_form_field(self, label_text):
        try:
            return self.find_form_field(label_text).is_displayed()
        except NoSuchElementException:
            return False

    def is_form_submit_visible(self):
        return self.is_visible(self.FORM_SUBMIT)

    @allure.step("Заполнить форму: имя '{name}', email '{email}', сообщение '{message}'")
    def fill_form(self, name="", email="", message=""):
        for label, value in (("Name", name), ("Email", email), ("Message", message)):
            field = self.find_form_field(label)
            field.clear()
            if value:
                field.send_keys(value)

    @allure.step("Нажать Submit в форме")
    def submit_form(self):
        self.click(self.FORM_SUBMIT)

    def is_form_valid(self):
        # встроенная проверка браузера: required и type=email
        form = self.driver.find_element(By.XPATH, FORM_XPATH + "//form")
        return self.driver.execute_script("return arguments[0].checkValidity();", form)

    def wait_form_success_visible(self, timeout=10):
        return self.wait_visible(self.FORM_SUCCESS, timeout)
