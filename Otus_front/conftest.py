import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.chrome.options import Options as ChromeOptions

url = "http://192.168.0.100:8081"
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Выбор браузера: chrome, firefox, safari")
    parser.addoption("--url", action="store", default="http://192.168.0.101:8081", help="URL для тестирования")
    parser.addoption("--headless", action="store_true", default=True, help="Запуск браузера в headless-режиме")


@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser")
    url = request.config.getoption("--url")
    headless = request.config.getoption("--headless")  # Получаем флаг headless

    try:
        if browser_name == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Chrome(service=ChromiumService(), options=options)

        elif browser_name == "firefox":
            options = FFOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(service=FFService(), options=options)

        elif browser_name == "safari":
            if headless:
                pytest.fail("Safari не поддерживает headless-режим")
            driver = webdriver.Safari()

        else:
            raise ValueError(f"Неподдерживаемый браузер: {browser_name}")

        driver.maximize_window()
        driver.get(url)

        yield driver  # Возвращаем драйвер для тестов

    except Exception as e:
        pytest.fail(f"Ошибка при инициализации браузера: {e}")

    finally:
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
