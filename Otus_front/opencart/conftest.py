import tempfile

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.chrome.options import Options as ChromeOptions

url = "http://192.168.0.105:8081"
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Выбор браузера: chrome, firefox, safari")
    parser.addoption("--url", action="store", default=url, help="URL для тестирования")
    parser.addoption("--headless", action="store_true", default=True, help="Запуск браузера в headless-режиме")
    parser.addoption("--remote", action="store_true", default=False, help="Запуск тестов удаленно через Selenoid")

@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser")
    url = request.config.getoption("--url")
    headless = request.config.getoption("--headless")
    remote = request.config.getoption("--remote")
    driver = None
    try:
        if remote:
            # Настройки для удаленного запуска через Selenoid
            if browser_name == "chrome":
                options = ChromeOptions()
                options.set_capability("browserName", "chrome")
                options.set_capability("browserVersion", "128.0")
                options.set_capability("selenoid:options", {
                    "enableVNC": True,
                    "enableVideo": False
                })
                if headless:
                    options.add_argument("--headless")
                driver = webdriver.Remote(
                    command_executor="http://192.168.0.105:4444/wd/hub/",
                    options=options
                )

            elif browser_name == "firefox":
                options = FFOptions()
                if headless:
                    options.add_argument("--headless")
                driver = webdriver.Remote(
                    command_executor="http://192.168.0.105:4444/wd/hub/",
                    options=options
                )

            elif browser_name == "safari":
                pytest.fail("Safari не поддерживается для удаленного запуска через Selenoid в данном примере")

            else:
                raise ValueError(f"Неподдерживаемый браузер: {browser_name}")

        else:
            # Локальный запуск
            if browser_name == "chrome":
                options = ChromeOptions()
                options.add_argument("--no-sandbox")  # Обязательно для Docker
                options.add_argument("--disable-dev-shm-usage")  # Решает проблемы с памятью
                options.add_argument("--remote-debugging-port=9222")  # Фиксированный порт
                options.add_argument("--user-data-dir=/tmp/chrome_profile")  # Уникальный каталог
                if headless:
                    options.add_argument("--headless")
                else:
                    # Для графического режима в контейнере
                    options.add_argument("--disable-gpu")
                    options.add_argument("--window-size=1920,1080")
                driver = webdriver.Chrome(service=ChromiumService(), options=options)

            elif browser_name == "firefox":
                options = FFOptions()
                options.add_argument("-profile")
                options.add_argument(tempfile.mkdtemp())
                if headless:
                    options.add_argument("--headless")
                else:
                    # Для графического режима в контейнере
                    options.add_argument("--disable-gpu")
                    options.add_argument("--window-size=1920,1080")
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

        if driver is not None:  # Проверяем, был ли driver инициализирован

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
