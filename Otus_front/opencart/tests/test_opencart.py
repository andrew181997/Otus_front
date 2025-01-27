
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from opencart.main_page_elements import MainPageLocators
from opencart.catalog_page_elements import CatalogPageLocators
from opencart.product_card_element import CardPageLocators
from opencart.admin_page_elements import AdminPageLocators
from opencart.registration_page_elements import RegPageLocators


def test_check_elements_home(browser):
    # Локаторы из класса MainPageLocators
    locators = [
        ("Cart Icon", MainPageLocators.CART_ICON),
        ("Logo", MainPageLocators.LOGO),
        ("Menu", MainPageLocators.MENU),
        ("Footer", MainPageLocators.FOOTER),
        ("Carousel Banner", MainPageLocators.CAROUSEL_BANNER),
        ("Search", MainPageLocators.SEARCH),
    ]

    # Проверка каждого локатора
    for name, locator in locators:
        element = WebDriverWait(browser, 3).until(
            EC.visibility_of_element_located(locator),
            message=f"{name} is not visible on the page"
        )
        assert element is not None, f"Element '{name}' was not found on the page"


def test_check_elements_product_card(browser):
    browser.get("http://192.168.0.101:8081/en-gb/product/desktops/apple-cinema")
    locators = [
        ("Container product", CardPageLocators.CONTAINER_PRODUCT),
        ("Product ikon", CardPageLocators.PRODUCT_ICON),
        ("Title product", CardPageLocators.TITLE_PRODUCT),
        ("Price new", CardPageLocators.PRICE_NEW),
        ("Add to wish list", CardPageLocators.ADD_TO_WISH_LIST),
        ("Button cart", CardPageLocators.BUTTON_CART),
    ]
    # Проверка каждого локатора
    for name, locator in locators:
        element = WebDriverWait(browser, 3).until(
            EC.visibility_of_element_located(locator),
            message=f"{name} is not visible on the page"
        )
        assert element is not None, f"Element '{name}' was not found on the page"

def test_check_elements_catalog(browser):
    browser.get("http://192.168.0.101:8081/en-gb/catalog/desktops")
    locators = [
        ("Left list", CatalogPageLocators.LEFT_LIST),
        ("Button home", CatalogPageLocators.BUTTON_HOME),
        ("Players", CatalogPageLocators.PLAYERS_IN_LEFT_LIST),
    ]
    # Проверка каждого локатора
    for name, locator in locators:
        element = WebDriverWait(browser, 3).until(
            EC.visibility_of_element_located(locator),
            message=f"{name} is not visible on the page"
        )
        assert element is not None, f"Element '{name}' was not found on the page"

def test_check_elements_admin(browser):
    browser.get("http://192.168.0.101:8081/administration/")
    locators = [
        ("Login form", AdminPageLocators.LOGIN_FORM),
        ("Input user name", AdminPageLocators.INPUT_USER_NAME),
        ("Input password", AdminPageLocators.INPUT_PASSWORD),
        ("Button login", AdminPageLocators.BUTTON_LOGIN),
    ]
    # Проверка каждого локатора
    for name, locator in locators:
        element = WebDriverWait(browser, 3).until(
            EC.visibility_of_element_located(locator),
            message=f"{name} is not visible on the page"
        )
        assert element is not None, f"Element '{name}' was not found on the page"

def test_check_elements_reg(browser):
    browser.get("http://192.168.0.101:8081/index.php?route=account/register")
    locators = [
        ("Input user name", RegPageLocators.INPUT_FIRST_NAME),
        ("Input last name", RegPageLocators.INPUT_LAST_NAME),
        ("Input email", RegPageLocators.INPUT_EMAIL),
        ("Input password", RegPageLocators.INPUT_PASSWORD),
        ("Switch subscribe", RegPageLocators.SWITCH_SUBSCRIBE),
        ("Switch privacy policy", RegPageLocators.SWITSH_PRIVACY_POLICY),
        ("Button registration", RegPageLocators.BUTTON_REG),
        ("Column right", RegPageLocators.COLUMN_RIGHT),
    ]
    # Проверка каждого локатора
    for name, locator in locators:
        element = WebDriverWait(browser, 3).until(
            EC.visibility_of_element_located(locator),
            message=f"{name} is not visible on the page"
        )
        assert element is not None, f"Element '{name}' was not found on the page"
