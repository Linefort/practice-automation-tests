import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage


class CalendarPage(BasePage):
    url = "https://practice-automation.com/calendars/"

    DATE_INPUT = (By.CSS_SELECTOR,
                  "input[placeholder='YYYY-MM-DD'], input.hasDatepicker, input[id*='selectorenteradate']")
    SUBMIT = (By.XPATH,
              "//input[@placeholder='YYYY-MM-DD']/ancestor::form//button[normalize-space()='Submit']")
    DATEPICKER = (By.ID, "ui-datepicker-div")
    NEXT_MONTH = (By.CSS_SELECTOR, "#ui-datepicker-div .ui-datepicker-next")
    PREV_MONTH = (By.CSS_SELECTOR, "#ui-datepicker-div .ui-datepicker-prev")
    DAYS = (By.CSS_SELECTOR, "#ui-datepicker-div td[data-handler='selectDay']")
    TODAY = (By.CSS_SELECTOR, "#ui-datepicker-div td.ui-datepicker-today")

    @property
    def value(self):
        return self.get_value(self.DATE_INPUT)

    def is_datepicker_visible(self):
        return self.is_visible(self.DATEPICKER)

    def shown_month(self):
        # у ячеек дня есть атрибуты data-year и data-month (месяц с нуля)
        cell = self.driver.find_element(*self.DAYS)
        return int(cell.get_attribute("data-year")), int(cell.get_attribute("data-month")) + 1

    def days_count(self):
        return len(self.driver.find_elements(*self.DAYS))

    def is_today_highlighted(self):
        return len(self.driver.find_elements(*self.TODAY)) > 0

    @allure.step("Открыть календарь кликом по полю даты")
    def open_datepicker(self):
        if not self.is_datepicker_visible():
            self.click(self.DATE_INPUT)
        assert self.wait_visible(self.DATEPICKER), "Календарь не открылся"

    @allure.step("Перейти в календаре к месяцу {target}")
    def go_to_month(self, target):
        year, month = self.shown_month()
        diff = (target.year - year) * 12 + target.month - month
        button = self.NEXT_MONTH if diff > 0 else self.PREV_MONTH
        for _ in range(abs(diff)):
            before = self.shown_month()
            self.click(button)
            self.wait_until(lambda: self.shown_month() != before)

    @allure.step("Выбрать дату {target} в календаре")
    def select_date(self, target):
        self.open_datepicker()
        self.go_to_month(target)
        day = (By.XPATH, f"//*[@id='ui-datepicker-div']//td[@data-handler='selectDay']"
                         f"/a[normalize-space()='{target.day}']")
        self.click(day)
        self.wait_invisible(self.DATEPICKER)

    @allure.step("Ввести дату вручную: {text}")
    def type_date(self, text):
        self.type_text(self.DATE_INPUT, text)

    @allure.step("Нажать Esc в поле даты")
    def press_escape_in_input(self):
        self.find(self.DATE_INPUT).send_keys(Keys.ESCAPE)

    @allure.step("Кликнуть по заголовку страницы (вне календаря)")
    def click_outside(self):
        ActionChains(self.driver).click(self.find_visible(self.HEADING)).perform()

    @allure.step("Нажать Submit")
    def submit(self):
        self.click(self.SUBMIT)
