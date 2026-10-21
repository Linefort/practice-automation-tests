import allure
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage

SIMPLE_MODAL = ("//div[(@role='dialog' or contains(@class, 'pum-container'))]"
                "[.//*[contains(normalize-space(), 'Simple Modal')]]")
FORM_MODAL = ("//div[(@role='dialog' or contains(@class, 'pum-container'))]"
              "[.//*[contains(normalize-space(), 'Modal Containing A Form')]]")
TITLE = "//*[contains(@class, 'pum-title') or contains(@class, 'popmake-title')]"
CONTENT = "//*[contains(@class, 'pum-content') or contains(@class, 'popmake-content')]"
CLOSE = "//*[contains(@class, 'pum-close') or contains(@class, 'popmake-close')]"


class ModalsPage(BasePage):
    url = "https://practice-automation.com/modals/"

    SIMPLE_BUTTON = (By.XPATH, "//*[@id='simple_modal' or "
                               "((self::button or self::a) and normalize-space()='Simple Modal')]")
    FORM_BUTTON = (By.XPATH, "//*[@id='form_modal' or "
                             "((self::button or self::a) and normalize-space()='Form Modal')]")

    SIMPLE = (By.XPATH, SIMPLE_MODAL)
    SIMPLE_TITLE = (By.XPATH, SIMPLE_MODAL + TITLE)
    SIMPLE_CONTENT = (By.XPATH, SIMPLE_MODAL + CONTENT)
    SIMPLE_CLOSE = (By.XPATH, SIMPLE_MODAL + CLOSE)

    FORM = (By.XPATH, FORM_MODAL)
    FORM_TITLE = (By.XPATH, FORM_MODAL + TITLE)
    FORM_CONTENT = (By.XPATH, FORM_MODAL + CONTENT)
    FORM_CLOSE = (By.XPATH, FORM_MODAL + CLOSE)
    FORM_SUBMIT = (By.XPATH, FORM_MODAL + "//button[normalize-space()='Submit']")
    FORM_SUCCESS = (By.XPATH, FORM_MODAL + "//*[contains(normalize-space(text()), 'Thank you for your response')]")

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

    @allure.step("Закрыть Simple Modal клавишей Esc")
    def close_simple_modal_by_escape(self):
        self.press_key(Keys.ESCAPE)

    @allure.step("Закрыть Form Modal кнопкой ×")
    def close_form_modal(self):
        self.click(self.FORM_CLOSE)

    def find_form_field(self, label_text):
        # у полей id генерируются автоматически, поэтому ищем по тексту label
        label = self.driver.find_element(
            By.XPATH, f"{FORM_MODAL}//label[starts-with(normalize-space(), '{label_text}')]")
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
        form = self.driver.find_element(By.XPATH, FORM_MODAL + "//form")
        return self.driver.execute_script("return arguments[0].checkValidity();", form)

    def is_form_success_visible(self):
        return self.is_visible(self.FORM_SUCCESS)
