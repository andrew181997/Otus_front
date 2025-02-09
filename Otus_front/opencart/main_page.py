import random
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains



class MainPageLocators:
    CART_ICON = (By.CLASS_NAME, "fa-cart-shopping")
    LOGO = (By.ID, "logo")
    MENU = (By.ID, "narbar-menu")
    FOOTER = (By.TAG_NAME, "footer")
    CAROUSEL_BANNER = (By.ID, "carousel-banner-1")
    SEARCH = (By.ID, "search")
    ADD_TO_CART = (By.XPATH, '//button[@formaction="http://192.168.0.101:8081/en-gb?route=checkout/cart.add"]')
    CART = (By.XPATH, "//a[text()='shopping cart']")
    FORM_CURRENCY = (By.ID, "form-currency")
    TABLE_CURRENCY = (By.XPATH, '//ul[@class="dropdown-menu show"]')


class MainPage():
    def __init__(self, browser):
        self.browser = browser


    def get_random_product(self):
        """Получает случайный товар на главной странице."""
        div_elements = WebDriverWait(self.browser, 3).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'col') and contains(@class, 'mb-3')]"))
        )
        random_div = random.choice(div_elements)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", random_div)
        time.sleep(1)
        return random_div

    def get_product_href(self, product_div):
        """Получает ссылку на товар."""
        name = product_div.find_element(By.TAG_NAME, "a")
        href_value = name.get_attribute('href')
        return href_value

    def add_product_to_cart(self, product_div):
        """Добавляет товар в корзину."""
        add_to_cart_button = product_div.find_element(By.XPATH, ".//button[@type='submit']")
        add_to_cart_button.click()

    def go_to_cart(self):
        """Переходит в корзину."""
        button_cart = WebDriverWait(self.browser, 2).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@href="http://192.168.0.100:8081/en-gb?route=checkout/cart"]'))
        )
        button_cart.click()

    def check_product_in_cart(self, href_value):
        """Проверяет, что товар есть в корзине."""
        cart_div = WebDriverWait(self.browser, 3).until(
            EC.presence_of_element_located((By.ID, "shopping-cart"))
        )
        links_in_cart = cart_div.find_elements(By.TAG_NAME, "a")
        found = False
        for link in links_in_cart:
            if link.get_attribute("href") == href_value:
                found = True
                break
        assert found, f"Элемент с ссылкой '{href_value}' не найден в корзине!"

    def select_random_currency(self):
        """Выбирает случайную валюту из выпадающего списка."""
        # Открываем выпадающий список валют
        form = WebDriverWait(self.browser, 2).until(
            EC.element_to_be_clickable((MainPageLocators.FORM_CURRENCY))
        )
        form.click()
        # Выбираем случайный элемент из списка валют
        dropdown_items = self.browser.find_elements(By.CSS_SELECTOR, "ul.dropdown-menu.show li")
        random_item = random.choice(dropdown_items)
        selected_currency = random_item.text[0]  # Первый символ текста (например, "$" или "€")
        random_item.click()
        return selected_currency

    def get_product_price(self):
        """Получает цену случайного товара."""
        main_page = MainPage(self.browser)
        random_product = main_page.get_random_product()
        price_element = random_product.find_element(By.CLASS_NAME, "price-new")
        price = price_element.text
        return price

    def navigate_to_desktops_catalog(self):
        """Открывает каталог 'Desktops'."""
        desktops = self.browser.find_element(By.CLASS_NAME, "nav-item.dropdown")  # Находит кнопку "Desktops"
        actions = ActionChains(self.browser)
        actions.move_to_element(desktops).perform()  # Наводит курсор на кнопку

        show_all_link = WebDriverWait(self.browser, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.see-all[href*='desktops']"))  # Ожидает кнопку перехода
        )
        show_all_link.click()
