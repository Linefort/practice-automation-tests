import allure


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

    @allure.title("Simple Modal закрывается клавишей Esc")
    def test_simple_modal_closes_by_escape(self, modals_page):
        modals_page.open_simple_modal()
        assert modals_page.wait_simple_modal_opened()
        modals_page.close_simple_modal_by_escape()
        assert modals_page.wait_simple_modal_closed(), "Simple Modal не закрылась по Esc"

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
        assert modals_page.wait_success_visible(), "Сообщение об отправке не появилось"


class TestModalsNegative:

    @allure.title("Пустая форма не отправляется")
    def test_empty_form_not_submitted(self, modals_page):
        modals_page.open_form_modal()
        assert modals_page.wait_form_modal_opened()
        modals_page.submit_form()
        assert not modals_page.is_form_valid()
        assert not modals_page.is_form_success_visible()
        assert modals_page.is_form_modal_visible()

    @allure.title("Форма без имени не отправляется, хотя остальные поля заполнены")
    def test_form_without_name_not_submitted(self, modals_page):
        modals_page.open_form_modal()
        assert modals_page.wait_form_modal_opened()
        modals_page.fill_form(email="test.user@example.com", message="Сообщение без имени")
        modals_page.submit_form()
        assert not modals_page.is_form_valid()
        assert not modals_page.is_form_success_visible()

    @allure.title("Email в неверном формате не принимается")
    def test_invalid_email_not_accepted(self, modals_page):
        modals_page.open_form_modal()
        assert modals_page.wait_form_modal_opened()
        modals_page.fill_form("Test User", "not-an-email", "Проверка email")
        modals_page.submit_form()
        assert not modals_page.is_form_valid()
        assert not modals_page.is_form_success_visible()

    @allure.title("При открытой Simple Modal Form Modal не отображается")
    def test_form_modal_hidden_when_simple_opened(self, modals_page):
        modals_page.open_simple_modal()
        assert modals_page.wait_simple_modal_opened()
        assert not modals_page.is_form_modal_visible()
