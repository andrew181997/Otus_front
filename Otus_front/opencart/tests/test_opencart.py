import time
import pytest

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from opencart.main_page import MainPageLocators, MainPage
from opencart.catalog_page_elements import CatalogPageLocators
from opencart.product_card_element import CardPageLocators
from opencart.admin_page_elements import AdminPageLocators, AdminPage
from opencart.registration_page_elements import RegPageLocators


@pytest.mark.parametrize("element_name, locator", [
    ("Cart Icon", MainPageLocators.CART_ICON),
    ("Logo", MainPageLocators.LOGO),
    ("Menu", MainPageLocators.MENU),
    ("Footer", MainPageLocators.FOOTER),
    ("Carousel Banner", MainPageLocators.CAROUSEL_BANNER),
    ("Search", MainPageLocators.SEARCH),
])
def test_check_element_visibility_home(browser, element_name, locator):
    """Проверяет, что основные элементы главной страницы отображаются."""
    browser.get("http://192.168.0.101:8081/")

    element = WebDriverWait(browser, 3).until(
        EC.visibility_of_element_located(locator),
        message=f"{element_name} is not visible on the page"
    )

    assert element is not None, f"Element '{element_name}' was not found on the page"


@pytest.mark.parametrize("element_name, locator", [
    ("Left list", CatalogPageLocators.LEFT_LIST),
    ("Button home", CatalogPageLocators.BUTTON_HOME),
    ("Players", CatalogPageLocators.PLAYERS_IN_LEFT_LIST),
])
def test_check_element_visibility_catalog(browser, element_name, locator):
    """Проверяет, что элементы каталога отображаются на странице."""
    browser.get("http://192.168.0.101:8081/en-gb/catalog/desktops")

    element = WebDriverWait(browser, 3).until(
        EC.visibility_of_element_located(locator),
        message=f"{element_name} is not visible on the page"
    )

    assert element is not None, f"Element '{element_name}' was not found on the page"

@pytest.mark.parametrize("element_name, locator", [
    ("Container product", CardPageLocators.CONTAINER_PRODUCT),
    ("Product icon", CardPageLocators.PRODUCT_ICON),
    ("Title product", CardPageLocators.TITLE_PRODUCT),
    ("Price new", CardPageLocators.PRICE_NEW),
    ("Add to wish list", CardPageLocators.ADD_TO_WISH_LIST),
    ("Button cart", CardPageLocators.BUTTON_CART),
])
def test_check_element_visibility_product_card(browser, element_name, locator):
    """Проверяет, что элементы карточки товара отображаются на странице."""
    browser.get("http://192.168.0.101:8081/en-gb/product/desktops/apple-cinema")

    element = WebDriverWait(browser, 3).until(
        EC.visibility_of_element_located(locator),
        message=f"{element_name} is not visible on the page"
    )

    assert element is not None, f"Element '{element_name}' was not found on the page"

@pytest.mark.parametrize("element_name, locator", [
    ("Login form", AdminPageLocators.LOGIN_FORM),
    ("Input user name", AdminPageLocators.INPUT_USER_NAME),
    ("Input password", AdminPageLocators.INPUT_PASSWORD),
    ("Button login", AdminPageLocators.BUTTON_LOGIN),
])
def test_check_element_visibility_admin(browser, element_name, locator):
    """Проверяет, что элементы страницы авторизации админ-панели отображаются."""
    browser.get("http://192.168.0.101:8081/administration/")

    element = WebDriverWait(browser, 3).until(
        EC.visibility_of_element_located(locator),
        message=f"{element_name} is not visible on the page"
    )

    assert element is not None, f"Element '{element_name}' was not found on the page"

@pytest.mark.parametrize("element_name, locator", [
    ("Input user name", RegPageLocators.INPUT_FIRST_NAME),
    ("Input last name", RegPageLocators.INPUT_LAST_NAME),
    ("Input email", RegPageLocators.INPUT_EMAIL),
    ("Input password", RegPageLocators.INPUT_PASSWORD),
    ("Switch subscribe", RegPageLocators.SWITCH_SUBSCRIBE),
    ("Switch privacy policy", RegPageLocators.SWITSH_PRIVACY_POLICY),
    ("Button registration", RegPageLocators.BUTTON_REG),
    ("Column right", RegPageLocators.COLUMN_RIGHT),
])
def test_check_element_visibility_reg(browser, element_name, locator):
    """Проверяет, что элементы формы регистрации отображаются на странице."""
    browser.get("http://192.168.0.101:8081/index.php?route=account/register")

    element = WebDriverWait(browser, 3).until(
        EC.visibility_of_element_located(locator),
        message=f"{element_name} is not visible on the page"
    )

    assert element is not None, f"Element '{element_name}' was not found on the page"


admin_url = "http://192.168.0.101:8081/administration/"
username = "user"
password = "bitnami"


def test_login_logout(browser):
    admin_page = AdminPage(browser)  # Передаем браузер в объект класса
    admin_page.open_admin_page("http://192.168.0.101:8081/administration/")
    admin_page.login(username, password)
    assert admin_page.is_logged_in(), "Логин не выполнен!"
    admin_page.logout()
    assert admin_page.is_logged_out(), "Разлогин не выполнен!"

def test_add_to_cart_new(browser):
    # Инициализация страницы
    main_page = MainPage(browser)
    # Шаг 1: Получить случайный товар
    random_product = main_page.get_random_product()
    # Шаг 2: Получить ссылку на товар
    href_value = main_page.get_product_href(random_product)
    # Шаг 3: Добавить товар в корзину
    main_page.add_product_to_cart(random_product)
    # Шаг 4: Перейти в корзину
    main_page.go_to_cart()
    # Шаг 5: Проверить, что товар есть в корзине
    main_page.check_product_in_cart(href_value)



def test_change_currency(browser):
    """Тест проверяет, что выбранная валюта соответствует валюте цены товара на главной ."""
    main_page = MainPage(browser)
    # Выбираем случайную валюту
    selected_currency = main_page.select_random_currency()
    time.sleep(3)
    # Получаем цену товара
    price = main_page.get_product_price()
    if selected_currency == "€":
        assert price[-1] == selected_currency,f"Ожидаемая валюта: {selected_currency}, фактическая валюта: {price[0]}"
    else:
        assert price[0] == selected_currency, f"Ожидаемая валюта: {selected_currency}, фактическая валюта: {price[0]}"



def test_change_currency_catalog(browser):
    """Тест проверяет, что выбранная валюта соответствует валюте цены товара на главной ."""

    main_page = MainPage(browser)
    # Выбираем случайную валюту
    selected_currency = main_page.select_random_currency()
    # Переходим в каталог
    main_page.navigate_to_desktops_catalog()
    # Записываем в переменную цену рандомного товара
    price = main_page.get_product_price()
    if selected_currency == "€":
        assert price[-1] == selected_currency, f"Ожидаемая валюта: {selected_currency}, фактическая валюта: {price[0]}"
    else:
        assert price[0] == selected_currency , f"Ожидаемая валюта: {selected_currency}, фактическая валюта: {price[0]}"
