import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption("--selenoid-url", action="store", default="http://localhost:4444/wd/hub")
    parser.addoption("--app-url", action="store", default="http://localhost:8080")
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--browser-version", action="store", default="latest")


@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser")

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
        "enableVideo": False
    })

    driver = webdriver.Remote(
        command_executor=request.config.getoption("--selenoid-url"),
        options=options  # Используем options вместо desired_capabilities
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
