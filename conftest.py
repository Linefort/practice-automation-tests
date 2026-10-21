import allure
import pytest
from selenium import webdriver

from pages.ads_page import AdsPage
from pages.calendar_page import CalendarPage
from pages.form_fields_page import FormFieldsPage
from pages.modals_page import ModalsPage


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     choices=["chrome", "firefox"], help="chrome или firefox")


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    if browser == "firefox":
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Chrome()
    driver.maximize_window()
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
