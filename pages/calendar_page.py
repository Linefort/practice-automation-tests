import calendar

import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage


class CalendarPage(BasePage):
    url = "https://practice-automation.com/calendars/"

    DATE_INPUT = (By.CSS_SELECTOR, "input[id*='selectorenteradate']")
    SUBMIT = (By.CSS_SELECTOR, "button.pushbutton-wide")

    # локаторы календаря взяты из реальной разметки (calendar_report.txt)
    DATEPICKER = (By.CSS_SELECTOR, ".dp-cal")
    MONTH = (By.CSS_SELECTOR, ".dp-cal-month")
    YEAR = (By.CSS_SELECTOR, ".dp-cal-year")
    NEXT_MONTH = (By.CSS_SELECTOR, ".dp-next")
    PREV_MONTH = (By.CSS_SELECTOR, ".dp-prev")
    # дни соседних месяцев в сетке помечены классом dp-edge-day
    DAYS = (By.CSS_SELECTOR, ".dp-cal button.dp-day:not(.dp-edge-day)")
    EDGE_DAYS = (By.CSS_SELECTOR, ".dp-cal button.dp-day.dp-edge-day")
    TODAY = (By.CSS_SELECTOR, ".dp-cal button.dp-day-today")

    @property
    def value(self):
        return self.get_value(self.DATE_INPUT)

    def is_datepicker_visible(self):
        return self.is_visible(self.DATEPICKER)

    def shown_year_month(self):
        month_name = self.find_visible(self.MONTH).text.strip()
        year = int(self.find_visible(self.YEAR).text.strip())
        return year, list(calendar.month_name).index(month_name)

    def days_count(self):
        return len(self.driver.find_elements(*self.DAYS))

    def edge_days_count(self):
        return len(self.driver.find_elements(*self.EDGE_DAYS))

    def is_today_highlighted(self):
        return len(self.driver.find_elements(*self.TODAY)) > 0

    @allure.step("Открыть календарь кликом по полю даты")
    def open_datepicker(self):
        if not self.is_datepicker_visible():
            self.click(self.DATE_INPUT)
            if not self.wait_visible(self.DATEPICKER, 3):
                # клик мог уйти до инициализации виджета - пробуем ещё раз через фокус
                self.driver.execute_script("arguments[0].focus()", self.find(self.DATE_INPUT))
        assert self.wait_visible(self.DATEPICKER), "Календарь не открылся"

    @allure.step("Перейти в календаре к месяцу {target}")
    def go_to_month(self, target):
        year, month = self.shown_year_month()
        diff = (target.year - year) * 12 + target.month - month
        button = self.NEXT_MONTH if diff > 0 else self.PREV_MONTH
        for _ in range(abs(diff)):
            before = self.shown_year_month()
            self.click(button)
            self.wait_until(lambda: self.shown_year_month() != before)

    @allure.step("Выбрать дату {target} в календаре")
    def select_date(self, target):
        self.open_datepicker()
        self.go_to_month(target)
        day = (By.XPATH, "//button[contains(@class, 'dp-day') and not(contains(@class, 'dp-edge-day')) "
                         f"and normalize-space()='{target.day}']")
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
