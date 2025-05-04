import time
import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .catalog_page_elements import CatalogPageLocators
from .product_card_element import CardPageLocators
from .admin_page_elements import AdminPageLocators, AdminPage
from .registration_page_elements import RegPageLocators, RegPage
from .main_page import MainPageLocators, MainPage


url = "http://192.168.0.105:8081"
@pytest.mark.parametrize("element_name, locator", [
    ("Cart Icon", MainPageLocators.CART_ICON),
    ("Logo", MainPageLocators.LOGO),
    ("Menu", MainPageLocators.MENU),
    ("Footer", MainPageLocators.FOOTER),
    ("Carousel Banner", MainPageLocators.CAROUSEL_BANNER),
    ("Search", MainPageLocators.SEARCH),
])
@allure.title("Отображение элементов главной страницы")
def test_check_element_visibility_home(browser, element_name, locator):
    """Проверяет, что основные элементы главной страницы отображаются."""
    browser.get(url)

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
@allure.title("Отображение элементов страницы каталога")
def test_check_element_visibility_catalog(browser, element_name, locator):
    """Проверяет, что элементы каталога отображаются на странице."""
    browser.get(f"{url}/en-gb/catalog/desktops")

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
@allure.title("Отображение элементов карточки товара")
def test_check_element_visibility_product_card(browser, element_name, locator):
    """Проверяет, что элементы карточки товара отображаются на странице."""
    browser.get(f"{url}/en-gb/product/desktops/apple-cinema")

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
@allure.title("Отображение элементов страницы логина админа")
def test_check_element_visibility_admin(browser, element_name, locator):
    """Проверяет, что элементы страницы авторизации админ-панели отображаются."""
    browser.get(f"{url}/administration/")

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
@allure.title("Отображение элементов страницы регистрации")
def test_check_element_visibility_reg(browser, element_name, locator):
    """Проверяет, что элементы формы регистрации отображаются на странице."""
    browser.get(f"{url}/index.php?route=account/register")

    element = WebDriverWait(browser, 3).until(
        EC.visibility_of_element_located(locator),
        message=f"{element_name} is not visible on the page"
    )

    assert element is not None, f"Element '{element_name}' was not found on the page"


admin_url = "http://192.168.0.105:8081/administration/"
username = "user"
password = "bitnami"

@allure.title("Логин и разлогин админа")
def test_login_logout(browser):
    """Тест проверяет логин и разлогин админа ."""
    admin_page = AdminPage(browser)
    with allure.step("Открываем страницу авторизации администратора"):
        admin_page.open_admin_page()
    with allure.step("Логинимся админом"):
        admin_page.login(username, password)
        assert admin_page.is_logged_in(), "Логин не выполнен!"
    with allure.step("Разлогиниваемся админом"):
        admin_page.logout()
    assert admin_page.is_logged_out(), "Разлогин не выполнен!"
@allure.title("Добавление товара в корзину")
def test_add_to_cart_new(browser):
    """Тест проверяет добавление товара в корзину ."""
    main_page = MainPage(browser)
    with allure.step("Получаем случайный товар"):
        random_product = main_page.get_random_product()
    with allure.step("Получаем ссылку на товар"):
        href_value = main_page.get_product_href(random_product)
    with allure.step("добавляем товар в корзину"):
        main_page.add_product_to_cart(random_product)
    with allure.step("Переходим в корзину"):
        main_page.go_to_cart()
    with allure.step("Проверка что товар есть в корзине"):
        main_page.check_product_in_cart(href_value)


@allure.title("Выбранная валюта соответствует валюте цены товара на главной")
def test_change_currency(browser):
    """Тест проверяет, что выбранная валюта соответствует валюте цены товара на главной ."""
    main_page = MainPage(browser)
    with allure.step("Выбираем случайную валюту"):
        selected_currency = main_page.select_random_currency()
    with allure.step("Получаем цену и валюту товара"):
        price = main_page.get_product_price()
    if selected_currency == "€":
        assert price[-1] == selected_currency,f"Ожидаемая валюта: {selected_currency}, фактическая валюта: {price[0]}"
    else:
        assert price[0] == selected_currency, f"Ожидаемая валюта: {selected_currency}, фактическая валюта: {price[0]}"


@allure.title("Выбранная валюта соответствует валюте цены товара в каталоге")
def test_change_currency_catalog(browser):
    """Тест проверяет, что выбранная валюта соответствует валюте цены товара в каталоге ."""
    main_page = MainPage(browser)
    with allure.step("Выбираем случайную валюту"):
        selected_currency = main_page.select_random_currency()
    with allure.step("Переходим в каталог"):
        main_page.navigate_to_desktops_catalog()
    with allure.step("Получаем цену и валюту товара"):
        price = main_page.get_product_price()
    if selected_currency == "€":
        assert price[-1] == selected_currency, f"Ожидаемая валюта: {selected_currency}, фактическая валюта: {price[0]}"
    else:
        assert price[0] == selected_currency , f"Ожидаемая валюта: {selected_currency}, фактическая валюта: {price[0]}"




@allure.title("Создание нового продукта админом")
def test_add_product_in_catalog(browser):
    """Тест проверяет создание нового продукта администратором."""
    admin_page = AdminPage(browser)
    product_name = "TEST_PHONE1"
    with allure.step("Открываем страницу авторизации администратора"):
        admin_page.open_admin_page()
    with allure.step("Логинимся админом"):
        admin_page.login(username, password)
    with allure.step("Переходим в каталог администратора"):
        admin_page.navigate_to_product_catalog()
    with allure.step("Создаем новый товар"):
        admin_page.add_new_product(product_name)
    with allure.step("находим созданный товар в каталоге"):
        result = admin_page.search_product_added(product_name)
    assert product_name in result

@allure.title("Удаление продукта из админки")
def test_delete_product(browser):
    """Тест проверяет удаление продукта из админки ."""
    admin_page = AdminPage(browser)
    product_name = "TEST_PHONE1"
    with allure.step("Открываем страницу авторизации администратора"):
        admin_page.open_admin_page()
    with allure.step("Логинимся админом"):
        admin_page.login(username, password)
    with allure.step("Переходим в каталог администратора"):
        admin_page.navigate_to_product_catalog()
    with allure.step("Создаем новый товар"):
        admin_page.add_new_product(product_name)
    with allure.step("Находим товар через фильтр"):
        admin_page.search_product_added(product_name)
    with allure.step("Удаляем товар"):
        admin_page.delete_product()
    with allure.step("Проверяем что не можем найти карточку товара на странице"):
        admin_page.assert_text_not_visible(product_name, AdminPageLocators.PRODUCT_CARD)
@allure.title("Регистрация пользователя")
def test_registration_member(browser):
    """Тест проверяет регистрацию обычного пользователя ."""
    reg_page = RegPage(browser)
    with allure.step("Открываем страницу регситрации пользователя"):
        reg_page.open_page_registartion()
    with allure.step("Регаем пользователя"):
        reg_page.rigistration_member()
    h1_element = WebDriverWait(browser, 4).until(
        EC.visibility_of_element_located(RegPageLocators.CHECK_REGISTRATION_BANNER))
    time.sleep(3)
    assert h1_element.text =="Your Account Has Been Created!"

