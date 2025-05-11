import random
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import logging



class MainPageLocators:
    CART_ICON = (By.CLASS_NAME, "fa-cart-shopping")
    LOGO = (By.ID, "logo")
    MENU = (By.ID, "narbar-menu")
    FOOTER = (By.TAG_NAME, "footer")
    CAROUSEL_BANNER = (By.ID, "carousel-banner-1")
    SEARCH = (By.ID, "search")
    ADD_TO_CART = (By.XPATH, '//button[@formaction="http://192.168.0.105/:8081/en-gb?route=checkout/cart.add"]')
    CART = (By.XPATH, "//a[text()='shopping cart']")
    FORM_CURRENCY = (By.ID, "form-currency")
    TABLE_CURRENCY = (By.XPATH, '//ul[@class="dropdown-menu show"]')


class MainPage:
    def __init__(self, browser):
        self.browser = browser

        self.logger = logging.getLogger(self.__class__.__name__)  # Логгер на основе имени класса
        self.logger.setLevel(logging.INFO)

    # Настроим формат логирования только один раз (если логгер уже создан, повторно не настраивать)
        if not self.logger.handlers:
            handler = logging.StreamHandler()  # Вывод в консоль (можно заменить на `FileHandler`)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def wait_and_click(self, locator):
        """Ожидает появления элемента и кликает по нему."""
        element = WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located(locator)
        )
        element.click()
        return element

    def wait_and_send_keys(self, locator, text):
        """Ожидает появления элемента и вводит текст."""
        element = WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located(locator)
        )
        element.send_keys(text)
        return element

    def wait_and_get_text(self, locator):
        """Ожидает появления элемента и возвращает его текст."""
        element = WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located(locator)
        )
        return element.text

    def get_random_product(self):
        """Получает случайный товар на главной странице."""
        self.logger.info("Выбираем случайный товар на главной странице.")
        div_elements = WebDriverWait(self.browser, 3).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'col') and contains(@class, 'mb-3')]"))
        )
        random_div = random.choice(div_elements)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", random_div)
        time.sleep(1)
        return random_div

    def get_product_href(self, product_div):
        """Получает ссылку на товар."""
        self.logger.info("Получаем ссылку на товар.")
        name = product_div.find_element(By.TAG_NAME, "a")
        href_value = name.get_attribute('href')
        self.logger.info(f"Ссылка на товар: {href_value}")
        return href_value

    def add_product_to_cart(self, product_div):
        """Добавляет товар в корзину."""
        self.logger.info("Добавляем товар в корзину.")
        add_to_cart_button = product_div.find_element(By.XPATH, ".//button[@type='submit']")
        add_to_cart_button.click()
        self.logger.info("Товар успешно добавлен в корзину.")

    def go_to_cart(self):
        """Переходит в корзину."""
        self.logger.info("Переходим в корзину.")
        button_cart = WebDriverWait(self.browser, 2).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@href="http://192.168.0.105:8081/en-gb?route=checkout/cart"]'))
        )
        button_cart.click()
        self.logger.info("Открыта корзина.")

    def check_product_in_cart(self, href_value):
        """Проверяет, что товар есть в корзине."""
        self.logger.info(f"Проверяем наличие товара в корзине: {href_value}")
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
        self.logger.info("Товар найден в корзине.")

    def select_random_currency(self):
        """Выбирает случайную валюту из выпадающего списка."""
        self.logger.info("Выбираем случайную валюту.")
        form = WebDriverWait(self.browser, 2).until(
            EC.element_to_be_clickable((MainPageLocators.FORM_CURRENCY))
        )
        form.click()
        # Выбираем случайный элемент из списка валют
        dropdown_items = self.browser.find_elements(By.CSS_SELECTOR, "ul.dropdown-menu.show li")
        random_item = random.choice(dropdown_items)
        selected_currency = random_item.text[0]  # Первый символ текста (например, "$" или "€")
        random_item.click()
        self.logger.info(f"Выбрана валюта: {selected_currency}")
        return selected_currency

    def get_product_price(self):
        """Получает цену случайного товара."""
        self.logger.info("Получаем цену случайного товара.")
        main_page = MainPage(self.browser)
        random_product = main_page.get_random_product()
        price_element = random_product.find_element(By.CLASS_NAME, "price-new")
        price = price_element.text
        self.logger.info(f"Цена товара: {price}")
        return price

    def navigate_to_desktops_catalog(self):
        """Открывает каталог 'Desktops'."""
        self.logger.info("Открываем каталог 'Desktops'.")
        desktops = self.browser.find_element(By.CLASS_NAME, "nav-item.dropdown")  # Находит кнопку "Desktops"
        actions = ActionChains(self.browser)
        actions.move_to_element(desktops).perform()  # Наводит курсор на кнопку

        show_all_link = WebDriverWait(self.browser, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.see-all[href*='desktops']"))  # Ожидает кнопку перехода
        )
        show_all_link.click()
        self.logger.info("Перешли в каталог 'Desktops'.")

