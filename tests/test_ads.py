import allure
from selenium.webdriver.common.keys import Keys


class TestAdsPositive:

    @allure.title("Страница открывается, заголовок Ads")
    def test_page_opened(self, ads_page):
        assert "Ads" in ads_page.title
        assert ads_page.heading == "Ads"

    @allure.title("На странице виден текст про отсчёт и описание")
    def test_intro_text_visible(self, ads_page):
        assert ads_page.is_intro_visible()
        assert ads_page.is_description_visible()

    @allure.title("Реклама появляется автоматически через несколько секунд")
    def test_ad_appears(self, ads_page):
        assert ads_page.wait_ad_opened(), "Реклама не появилась"

    @allure.title("В рекламном окне есть текст I am an ad")
    def test_ad_text(self, ads_page):
        assert ads_page.wait_ad_opened()
        assert "I am an ad" in ads_page.ad_text()

    @allure.title("Заголовок рекламного окна - Hi")
    def test_ad_title(self, ads_page):
        assert ads_page.wait_ad_opened()
        assert ads_page.ad_title() == "Hi"

    @allure.title("В рекламном окне отображается кнопка закрытия")
    def test_ad_close_button_visible(self, ads_page):
        assert ads_page.wait_ad_opened()
        assert ads_page.is_ad_close_button_visible()

    @allure.title("Реклама закрывается кнопкой ×")
    def test_ad_closes_by_button(self, ads_page):
        assert ads_page.wait_ad_opened()
        ads_page.close_ad()
        assert ads_page.wait_ad_closed(), "Реклама осталась на экране"

    @allure.title("Реклама закрывается клавишей Esc")
    def test_ad_closes_by_escape(self, ads_page):
        assert ads_page.wait_ad_opened()
        ads_page.close_ad_by_escape()
        assert ads_page.wait_ad_closed(), "Реклама не закрылась по Esc"

    @allure.title("После закрытия рекламы ссылка Learn More доступна")
    def test_page_available_after_ad_closed(self, ads_page):
        assert ads_page.wait_ad_opened()
        ads_page.close_ad()
        assert ads_page.wait_ad_closed()
        assert ads_page.is_learn_more_reachable(), "Ссылка Learn More перекрыта"
        assert "linktr.ee" in ads_page.learn_more_href

    @allure.title("Если не закрывать рекламу, после обновления страницы она появляется снова")
    def test_ad_appears_after_reload(self, ads_page):
        assert ads_page.wait_ad_opened()
        ads_page.reload()
        assert ads_page.wait_ad_opened(), "После обновления реклама не появилась"


class TestAdsNegative:

    @allure.title("Закрытая реклама не появляется повторно на той же странице")
    def test_ad_does_not_reappear(self, ads_page):
        assert ads_page.wait_ad_opened()
        ads_page.close_ad()
        assert ads_page.wait_ad_closed()
        assert ads_page.ad_stays_hidden(8), "Реклама появилась снова"

    @allure.title("Вместе с рекламой не открываются другие модальные окна")
    def test_other_modals_hidden_with_ad(self, ads_page):
        assert ads_page.wait_ad_opened()
        assert not ads_page.is_simple_modal_visible()
        assert not ads_page.is_form_modal_visible()

    @allure.title("Посторонние клавиши (Tab, X, стрелка вниз) не закрывают рекламу")
    def test_other_keys_do_not_close_ad(self, ads_page):
        assert ads_page.wait_ad_opened()
        for key in (Keys.TAB, "x", Keys.ARROW_DOWN):
            ads_page.press_key(key)
        assert ads_page.is_ad_visible(), "Реклама закрылась от постороннего нажатия"

    @allure.title("Пока открыта реклама, ссылки под ней недоступны")
    def test_page_blocked_while_ad_open(self, ads_page):
        assert ads_page.wait_ad_opened()
        assert not ads_page.is_learn_more_reachable(), "Ссылка доступна при открытой рекламе"
