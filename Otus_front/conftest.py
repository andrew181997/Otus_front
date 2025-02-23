import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.firefox.service import Service as FFService

url = "http://192.168.0.100:8081"
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Выбор браузера: chrome, firefox, safari")
    parser.addoption("--url", action="store", default="http://192.168.0.101:8081", help="URL для тестирования")


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption("--browser")
    url = request.config.getoption("--url")

    try:
        if browser_name == "chrome":
            driver = webdriver.Chrome(service=ChromiumService())
        elif browser_name == "firefox":
            driver = webdriver.Firefox(options=FFOptions(), service=FFService())
        elif browser_name == "safari":
            driver = webdriver.Safari()
        else:
            raise ValueError(f"Неподдерживаемый браузер: {browser_name}")

        driver.maximize_window()
        driver.get(url)

        yield driver  # Возвращаем драйвер для использования в тестах

    except Exception as e:
        pytest.fail(f"Ошибка при инициализации браузера: {e}")

    finally:
        driver.quit()