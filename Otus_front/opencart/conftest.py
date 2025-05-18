import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption("--selenoid-url", action="store", default="http://192.168.0.105:4444/wd/hub")
    parser.addoption("--app-url", action="store", default="http://192.168.0.105:8081")
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--browser-version", action="store", default="128.0")
    parser.addoption("--local", action="store_true", help="Run tests locally instead of Selenoid")

@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser")
    is_local = request.config.getoption("--local")

    if is_local:
        # Локальный запуск браузера
        if browser_name == "chrome":
            options = ChromeOptions()
            # Добавьте нужные опции для Chrome
            # options.add_argument("--headless")  # для headless режима
            driver = webdriver.Chrome(options=options)
        elif browser_name == "firefox":
            options = FirefoxOptions()
            # Добавьте нужные опции для Firefox
            # options.add_argument("-headless")  # для headless режима
            driver = webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
    else:
        # Удалённый запуск через Selenoid
        if browser_name == "chrome":
            options = ChromeOptions()
        elif browser_name == "firefox":
            options = FirefoxOptions()
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        options.set_capability("browserName", browser_name)
        options.set_capability("browserVersion", request.config.getoption("--browser-version"))
        options.set_capability("selenoid:options", {
            "enableVNC": True,
            "enableVideo": True
        })

        driver = webdriver.Remote(
            command_executor=request.config.getoption("--selenoid-url"),
            options=options
        )

    driver.get(request.config.getoption("--app-url"))
    driver.maximize_window()  # Опционально: максимизировать окно
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
