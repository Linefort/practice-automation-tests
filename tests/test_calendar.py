from calendar import monthrange
from datetime import date

import allure
import pytest

today = date.today()


def month_shift(months):
    # 15 число есть в любом месяце
    index = today.year * 12 + today.month - 1 + months
    return date(index // 12, index % 12 + 1, 15)


class TestCalendarPositive:

    @allure.title("Страница календаря открывается, заголовок Calendars")
    def test_page_opened(self, calendar_page):
        assert "Calendars" in calendar_page.title
        assert calendar_page.heading == "Calendars"

    @allure.title("Клик по полю даты открывает календарь")
    def test_datepicker_opens(self, calendar_page):
        calendar_page.open_datepicker()
        assert calendar_page.is_datepicker_visible()

    @allure.title("Календарь открывается на текущем месяце и годе")
    def test_current_month_shown(self, calendar_page):
        calendar_page.open_datepicker()
        assert calendar_page.shown_year_month() == (today.year, today.month)

    @allure.title("Сегодняшний день выделен в календаре")
    def test_today_highlighted(self, calendar_page):
        calendar_page.open_datepicker()
        assert calendar_page.is_today_highlighted()

    @allure.title("Выбор сегодняшней даты записывает её в поле в формате ГГГГ-ММ-ДД")
    def test_select_today(self, calendar_page):
        calendar_page.select_date(today)
        assert calendar_page.value == today.isoformat()

    @allure.title("Выбор даты в прошлом месяце, следующем месяце и другом году")
    @pytest.mark.parametrize("months", [-1, 1, 14],
                             ids=["прошлый месяц", "следующий месяц", "через 14 месяцев"])
    def test_select_shifted_date(self, calendar_page, months):
        target = month_shift(months)
        calendar_page.select_date(target)
        assert calendar_page.value == target.isoformat()

    @allure.title("Дату можно ввести вручную в формате ГГГГ-ММ-ДД")
    def test_type_date_manually(self, calendar_page):
        calendar_page.type_date("2025-01-15")
        assert calendar_page.value == "2025-01-15"

    @allure.title("Форма с выбранной датой отправляется, появляется подтверждение")
    def test_submit_selected_date(self, calendar_page):
        calendar_page.select_date(month_shift(2))
        calendar_page.submit()
        assert calendar_page.wait_success_visible(), "Сообщение об отправке не появилось"


class TestCalendarNegative:

    @allure.title("Календарь скрыт, пока не кликнули по полю даты")
    def test_datepicker_hidden_by_default(self, calendar_page):
        assert not calendar_page.is_datepicker_visible()

    @allure.title("Клик вне календаря закрывает его, поле остаётся пустым")
    def test_click_outside_closes_datepicker(self, calendar_page):
        calendar_page.open_datepicker()
        calendar_page.click_outside()
        assert calendar_page.wait_datepicker_closed(), "Календарь не закрылся"
        assert calendar_page.value == ""

    @allure.title("Esc закрывает календарь, дата не выбирается")
    def test_escape_closes_datepicker(self, calendar_page):
        calendar_page.open_datepicker()
        calendar_page.press_escape_in_input()
        assert calendar_page.wait_datepicker_closed(), "Календарь не закрылся"
        assert calendar_page.value == ""

    @allure.title("Дни соседних месяцев в сетке отмечены отдельно и не входят в текущий месяц")
    def test_adjacent_month_days_are_separate(self, calendar_page):
        calendar_page.open_datepicker()
        assert calendar_page.days_count() == monthrange(today.year, today.month)[1]
        assert calendar_page.edge_days_count() > 0
