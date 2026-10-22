import logging

import allure
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from pages.ads_page import AdsPage
from pages.calendar_page import CalendarPage
from pages.form_fields_page import FormFieldsPage
from pages.modals_page import ModalsPage

# selenium manager пишет безобидные WARNING про кэш-папку на Windows - прячем их
logging.getLogger("selenium.webdriver.common.selenium_manager").setLevel(logging.ERROR)

# сторонние рекламные и аналитические домены: на проверки не влияют, а загрузку тормозят
BLOCKED_URLS = ["*google-analytics.com*", "*googletagmanager.com*", "*googlesyndication.com*",
                "*doubleclick.net*", "*googleadservices.com*", "*connect.facebook.net*"]


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     choices=["chrome", "firefox"], help="chrome или firefox")
    parser.addoption("--headless", action="store_true",
                     help="запуск браузера без интерфейса")


def create_chrome(headless):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-search-engine-choice-screen")
    options.add_argument("--disable-features=Translate")
    # eager: get() возвращается после разбора html, до полной загрузки ресурсов;
    # готовность скриптов дожидается в BasePage.open()
    options.page_load_strategy = "eager"
    driver = webdriver.Chrome(options=options)
    try:
        # блокировка мусорных доменов через DevTools Protocol, есть только у Chrome
        driver.execute_cdp_cmd("Network.enable", {})
        driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": BLOCKED_URLS})
    except WebDriverException:
        pass
    return driver


def create_firefox(headless):
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("-headless")
    return webdriver.Firefox(options=options)


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    driver = create_firefox(headless) if browser == "firefox" else create_chrome(headless)

    if headless:
        driver.set_window_size(1920, 1080)
    else:
        try:
            driver.maximize_window()
        except WebDriverException:
            driver.set_window_size(1920, 1080)

    driver.set_page_load_timeout(60)
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when in ("setup", "call") and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(driver.get_screenshot_as_png(), name="Скриншот при ошибке",
                          attachment_type=allure.attachment_type.PNG)


@pytest.fixture
def calendar_page(driver):
    page = CalendarPage(driver)
    page.open()
    return page


@pytest.fixture
def modals_page(driver):
    page = ModalsPage(driver)
    page.open()
    return page


@pytest.fixture
def ads_page(driver):
    page = AdsPage(driver)
    page.open()
    return page


@pytest.fixture
def form_fields_page(driver):
    page = FormFieldsPage(driver)
    page.open()
    return page
