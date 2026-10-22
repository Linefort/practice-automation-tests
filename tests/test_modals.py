import allure
import pytest
from selenium.webdriver.common.keys import Keys


class TestModalsPositive:

    @allure.title("Страница открывается, заголовок Modals, обе кнопки на месте")
    def test_page_opened(self, modals_page):
        assert "Modals" in modals_page.title
        assert modals_page.heading == "Modals"
        assert modals_page.is_simple_button_visible()
        assert modals_page.is_form_button_visible()

    @allure.title("После загрузки страницы обе модалки скрыты")
    def test_modals_hidden_by_default(self, modals_page):
        assert not modals_page.is_simple_modal_visible()
        assert not modals_page.is_form_modal_visible()

    @allure.title("Simple Modal открывается по кнопке")
    def test_simple_modal_opens(self, modals_page):
        modals_page.open_simple_modal()
        assert modals_page.wait_simple_modal_opened(), "Simple Modal не появилась"

    @allure.title("Simple Modal содержит заголовок и текст")
    def test_simple_modal_content(self, modals_page):
        modals_page.open_simple_modal()
        assert modals_page.wait_simple_modal_opened()
        assert modals_page.simple_modal_title() == "Simple Modal"
        assert "a simple modal" in modals_page.simple_modal_text()

    @allure.title("Simple Modal закрывается кнопкой ×")
    def test_simple_modal_closes_by_button(self, modals_page):
        modals_page.open_simple_modal()
        assert modals_page.wait_simple_modal_opened()
        modals_page.close_simple_modal()
        assert modals_page.wait_simple_modal_closed(), "Simple Modal осталась на экране"

    @allure.title("Simple Modal можно открыть повторно после закрытия")
    def test_simple_modal_reopens(self, modals_page):
        modals_page.open_simple_modal()
        assert modals_page.wait_simple_modal_opened()
        modals_page.close_simple_modal()
        assert modals_page.wait_simple_modal_closed()
        modals_page.open_simple_modal()
        assert modals_page.wait_simple_modal_opened(), "Simple Modal не открылась повторно"

    @allure.title("Form Modal открывается, виден заголовок и подсказка")
    def test_form_modal_opens(self, modals_page):
        modals_page.open_form_modal()
        assert modals_page.wait_form_modal_opened(), "Form Modal не появилась"
        assert modals_page.form_modal_title() == "Modal Containing A Form"
        assert "Please enter your contact info below" in modals_page.form_modal_text()

    @allure.title("В Form Modal есть поля Name, Email, Message и кнопка Submit")
    def test_form_modal_fields(self, modals_page):
        modals_page.open_form_modal()
        assert modals_page.wait_form_modal_opened()
        for label in ("Name", "Email", "Message"):
            assert modals_page.has_form_field(label), f"Нет поля {label}"
        assert modals_page.is_form_submit_visible()

    @allure.title("Form Modal закрывается кнопкой ×")
    def test_form_modal_closes_by_button(self, modals_page):
        modals_page.open_form_modal()
        assert modals_page.wait_form_modal_opened()
        modals_page.close_form_modal()
        assert modals_page.wait_form_modal_closed(), "Form Modal осталась на экране"

    @allure.title("Форма с корректными данными отправляется, появляется подтверждение")
    def test_form_modal_valid_submit(self, modals_page):
        modals_page.open_form_modal()
        assert modals_page.wait_form_modal_opened()
        modals_page.fill_form("Test User", "test.user@example.com", "Автотест: отправка формы")
        assert modals_page.is_form_valid()
        modals_page.submit_form()
        assert modals_page.wait_form_success_visible(), "Сообщение об отправке не появилось"


class TestModalsNegative:

    @allure.title("Сайт не валидирует форму: пустая форма принимается, появляется подтверждение")
    def test_empty_form_is_accepted(self, modals_page):
        modals_page.open_form_modal()
        assert modals_page.wait_form_modal_opened()
        # браузерная валидация данные не принимает, но у формы novalidate - сайт всё равно шлёт
        assert not modals_page.is_form_valid()
        modals_page.submit_form()
        assert modals_page.wait_form_success_visible(), "Пустую форму сайт не принял"

    @allure.title("Сайт не проверяет email: некорректные значения принимаются")
    @pytest.mark.parametrize("email", ["not-an-email", "test@", "@example.com"],
                             ids=["без собаки", "без домена", "без имени пользователя"])
    def test_invalid_email_is_accepted(self, modals_page, email):
        modals_page.open_form_modal()
        assert modals_page.wait_form_modal_opened()
        modals_page.fill_form("Test User", email, "Проверка отсутствия валидации")
        assert not modals_page.is_form_valid()
        modals_page.submit_form()
        assert modals_page.wait_form_success_visible(), f"Email '{email}' сайт не принял"

    @allure.title("Клавиша Esc не закрывает Simple Modal")
    def test_escape_does_not_close_simple_modal(self, modals_page):
        modals_page.open_simple_modal()
        assert modals_page.wait_simple_modal_opened()
        modals_page.press_key(Keys.ESCAPE)
        assert modals_page.simple_modal_stays_open(2), "Simple Modal закрылась по Esc"

    @allure.title("При открытой Simple Modal Form Modal не отображается")
    def test_form_modal_hidden_when_simple_opened(self, modals_page):
        modals_page.open_simple_modal()
        assert modals_page.wait_simple_modal_opened()
        assert not modals_page.is_form_modal_visible()
