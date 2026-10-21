import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage

AD_XPATH = ("//div[(@role='dialog' or contains(@class, 'pum-container'))]"
            "[.//*[contains(normalize-space(), 'I am an ad')]]")
SIMPLE_MODAL_XPATH = ("//div[(@role='dialog' or contains(@class, 'pum-container'))]"
                      "[.//*[contains(normalize-space(), 'Simple Modal')]]")
FORM_MODAL_XPATH = ("//div[(@role='dialog' or contains(@class, 'pum-container'))]"
                    "[.//*[contains(normalize-space(), 'Modal Containing A Form')]]")


class AdsPage(BasePage):
    url = "https://practice-automation.com/ads/"
    AD_TIMEOUT = 20

    INTRO = (By.XPATH, "//*[contains(normalize-space(text()), 'An ad will appear in')]")
    DESCRIPTION = (By.XPATH, "//*[contains(normalize-space(text()), 'Do you love watching ads')]")
    LEARN_MORE = (By.XPATH, "//a[normalize-space()='Learn More']")

    AD = (By.XPATH, AD_XPATH)
    AD_TITLE = (By.XPATH, AD_XPATH + "//*[contains(@class, 'pum-title') or contains(@class, 'popmake-title')]")
    AD_CONTENT = (By.XPATH, AD_XPATH + "//*[contains(@class, 'pum-content') or contains(@class, 'popmake-content')]")
    AD_CLOSE = (By.XPATH, AD_XPATH + "//*[contains(@class, 'pum-close') or contains(@class, 'popmake-close')]")
    SIMPLE_MODAL = (By.XPATH, SIMPLE_MODAL_XPATH)
    FORM_MODAL = (By.XPATH, FORM_MODAL_XPATH)

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
        return self.is_visible(self.AD_CLOSE)

    @allure.step("Закрыть рекламу кнопкой ×")
    def close_ad(self):
        self.click(self.AD_CLOSE)

    @allure.step("Закрыть рекламу клавишей Esc")
    def close_ad_by_escape(self):
        self.press_key(Keys.ESCAPE)

    @allure.step("Подождать {seconds} сек и проверить, что реклама не появилась")
    def ad_stays_hidden(self, seconds):
        return self.stays_hidden(self.AD, seconds)

    def is_simple_modal_visible(self):
        return self.is_visible(self.SIMPLE_MODAL)

    def is_form_modal_visible(self):
        return self.is_visible(self.FORM_MODAL)

    @allure.step("Проверить, доступна ли ссылка Learn More для клика")
    def is_learn_more_reachable(self):
        return self.is_reachable(self.LEARN_MORE)

    @property
    def learn_more_href(self):
        return self.find(self.LEARN_MORE).get_attribute("href")

    @allure.step("Обновить страницу")
    def reload(self):
        self.driver.refresh()
