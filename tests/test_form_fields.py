import allure


class TestFormFields:

    @allure.title("Поле Message заполняется списком из раздела Automation Tools через запятую")
    def test_message_filled_with_automation_tools(self, form_fields_page):
        tools = form_fields_page.get_automation_tools()
        assert tools, "Список Automation Tools пуст"

        text = ", ".join(tools)
        form_fields_page.fill_message(text)

        assert form_fields_page.message_value == text

    @allure.title("В списке Automation Tools есть Selenium")
    def test_tools_contain_selenium(self, form_fields_page):
        assert "Selenium" in form_fields_page.get_automation_tools()

    @allure.title("Заполненная форма отправляется, появляется алерт Message received!")
    def test_submit_shows_alert(self, form_fields_page):
        form_fields_page.fill_personal_data("Test User", "Passw0rd!", "test.user@example.com")
        form_fields_page.fill_message(", ".join(form_fields_page.get_automation_tools()))
        form_fields_page.submit()
        assert form_fields_page.accept_alert() == "Message received!"
