import tempfile

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.chrome.options import Options as ChromeOptions


def pytest_addoption(parser):
    parser.addoption("--selenoid-url", help="Selenoid hub URL")
    parser.addoption("--app-url", help="Application URL")
    parser.addoption("--browser", help="Browser name")
    parser.addoption("--browser-version", help="Browser version")


@pytest.fixture
def browser(request):
    options = {
        "browserName": request.config.getoption("--browser"),
        "browserVersion": request.config.getoption("--browser-version"),
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": False
        }
    }

    driver = webdriver.Remote(
        command_executor=request.config.getoption("--selenoid-url"),
        desired_capabilities=options
    )

    driver.get(request.config.getoption("--app-url"))
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Фикстура для создания отчёта о результате теста."""
    outcome = yield
    rep = outcome.get_result()
    # Проверяем, что тест упал
    if rep.when == "call" and rep.failed:
        # Получаем объект браузера из фикстуры
        browser = item.funcargs.get("browser")
        if browser:
            # Делаем скриншот
            allure.attach(
                browser.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
