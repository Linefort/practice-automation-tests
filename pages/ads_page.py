import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.popup_page import CLOSE, CONTENT, TITLE, popup_xpath

AD_XPATH = popup_xpath("I am an ad")


class AdsPage(BasePage):
    url = "https://practice-automation.com/ads/"
    AD_TIMEOUT = 20

    INTRO = (By.XPATH, "//*[contains(normalize-space(text()), 'An ad will appear in')]")
    DESCRIPTION = (By.XPATH, "//*[contains(normalize-space(text()), 'Do you love watching ads')]")
    LEARN_MORE = (By.XPATH, "//a[normalize-space()='Learn More']")

    AD = (By.XPATH, AD_XPATH)
    AD_TITLE = (By.XPATH, AD_XPATH + TITLE)
    AD_CONTENT = (By.XPATH, AD_XPATH + CONTENT)
    AD_CLOSE = (By.XPATH, AD_XPATH + CLOSE)
    SIMPLE_MODAL = (By.XPATH, popup_xpath("Simple Modal"))
    FORM_MODAL = (By.XPATH, popup_xpath("Modal Containing A Form"))

    def wait_page_ready(self):
        # Popup Maker создаёт оверлеи при инициализации - сигнал, что скрипты окон готовы
        self.wait_until(lambda: self.driver.execute_script(
            "return document.querySelectorAll('.pum-overlay').length > 0"), 10)

    def is_intro_visible(self):
        return self.is_visible(self.INTRO)

    def is_description_visible(self):
        return self.is_visible(self.DESCRIPTION)

    @allure.step("Дождаться появления рекламы")
    def wait_ad_opened(self):
        return self.wait_visible(self.AD, self.AD_TIMEOUT)

    def wait_ad_closed(self):
        return self.wait_invisible(self.AD)

    def is_ad_visible(self):
        return self.is_visible(self.AD)

    def ad_title(self):
        return self.get_text(self.AD_TITLE)

    def ad_text(self):
        return self.get_text(self.AD_CONTENT)

    def is_ad_close_button_visible(self):
        # кнопка может отрисоваться с задержкой после появления окна
        return self.wait_visible(self.AD_CLOSE, 5)

    @allure.step("Закрыть рекламу кнопкой ×")
    def close_ad(self):
        self.click(self.AD_CLOSE)

    @allure.step("Подождать {seconds} сек и проверить, что реклама не появилась")
    def ad_stays_hidden(self, seconds):
        return self.stays_hidden(self.AD, seconds)

    @allure.step("Подождать {seconds} сек и проверить, что реклама осталась открытой")
    def ad_stays_open(self, seconds):
        return self.stays_visible(self.AD, seconds)

    def is_simple_modal_visible(self):
        return self.is_visible(self.SIMPLE_MODAL)

    def is_form_modal_visible(self):
        return self.is_visible(self.FORM_MODAL)

    def is_learn_more_reachable(self):
        return self.is_reachable(self.LEARN_MORE)

    @allure.step("Дождаться, пока ссылка Learn More станет доступна для клика")
    def wait_learn_more_reachable(self):
        # после закрытия рекламы затемнение пропадает не мгновенно
        return self.wait_until(self.is_learn_more_reachable)

    @property
    def learn_more_href(self):
        return self.find(self.LEARN_MORE).get_attribute("href")

    @allure.step("Обновить страницу")
    def reload(self):
        self.driver.refresh()
