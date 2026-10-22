import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class FormFieldsPage(BasePage):
    url = "https://practice-automation.com/form-fields/"

    NAME = (By.ID, "name-input")
    PASSWORD = (By.CSS_SELECTOR, "input[type='password']")
    EMAIL = (By.ID, "email")
    MESSAGE = (By.ID, "message")
    SUBMIT = (By.ID, "submit-btn")
    # список лежит сразу под заголовком Automation tools, регистр букв в разметке может отличаться
    AUTOMATION_TOOLS = (By.XPATH,
                        "//*[contains(translate(normalize-space(text()), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                        "'abcdefghijklmnopqrstuvwxyz'), 'automation tools')]/following::ul[1]/li")

    @property
    def message_value(self):
        return self.get_value(self.MESSAGE)

    @allure.step("Получить список элементов из раздела Automation Tools")
    def get_automation_tools(self):
        items = self.wait.until(EC.presence_of_all_elements_located(self.AUTOMATION_TOOLS))
        return [item.text.strip() for item in items if item.text.strip()]

    @allure.step("Ввести текст в поле Message")
    def fill_message(self, text):
        self.type_text(self.MESSAGE, text)

    @allure.step("Заполнить поля Name, Password и Email")
    def fill_personal_data(self, name, password, email):
        self.type_text(self.NAME, name)
        self.type_text(self.PASSWORD, password)
        self.type_text(self.EMAIL, email)

    @allure.step("Нажать Submit")
    def submit(self):
        self.click(self.SUBMIT)

    @allure.step("Дождаться алерта и принять его")
    def accept_alert(self):
        alert = self.wait.until(EC.alert_is_present())
        text = alert.text
        alert.accept()
        return text
