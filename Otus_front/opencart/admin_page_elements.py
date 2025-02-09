from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait



class AdminPageLocators:
    LOGIN_FORM = (By.ID, "form-login")
    INPUT_USER_NAME = (By.ID, "input-username")
    INPUT_PASSWORD = (By.ID, "input-password")
    BUTTON_LOGIN = (By.XPATH, '//button[contains(text(), " Login")]')
    BUTTON_LOGOUT = (By.ID, "nav-logout")

    CATALOG = (By.ID, "menu-catalog")
    PRODUCTS = (By.XPATH, "//a[text()='Products']")
    ADD_PRODUCT = (By.CLASS_NAME, 'fa-solid.fa-plus')
    INPUT_PRODUCT_NAME = (By.ID, 'input-name-1')
    INPUT_META_TAG_TITLE = (By.ID, 'input-meta-title-1')
    DATA_PRODUCT = (By.XPATH, "//a[text()='Data']")
    INPUT_MODEL = (By.ID, 'input-model')
    SEO_PRODUCT = (By.XPATH, "//a[text()='SEO']")
    INPUT_SEO = (By.ID, 'input-keyword-0-1')
    BUTTON_SAVE_PRODUCT = (By.CLASS_NAME, 'fa-solid.fa-floppy-disk')
    BUTTON_BACK = (By.CLASS_NAME, 'fa-solid.fa-reply')
    INPUT_FILTER_PRODUCT_NAME = (By.ID, 'input-name')
    BUTTON_FILTER = (By.ID, 'button-filter')
    PRODUCT_CARD = (By.XPATH, "(//td[contains(@class, 'text-start')])[3]") #form-product > div.table-responsive > table > tbody > tr:nth-child(1) > td:nth-child(3)
    CHECK_BOX_CARD = (By.XPATH, "//input[@type='checkbox']")
    BUTTON_DELETE_PRODUCT = (By.CLASS_NAME, 'fa-regular.fa-trash-can')



class AdminPage:
    def __init__(self, browser):
        self.browser = browser

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



    def open_admin_page(self):
        self.browser.get("http://192.168.0.101:8081/administration")

    def login(self, username, password):
        self.wait_and_send_keys(AdminPageLocators.INPUT_USER_NAME, username)
        self.wait_and_send_keys(AdminPageLocators.INPUT_PASSWORD, password)
        self.wait_and_click(AdminPageLocators.BUTTON_LOGIN)


    def is_logged_in(self):
        try:
            WebDriverWait(self.browser, 3).until(
                EC.visibility_of_element_located((AdminPageLocators.BUTTON_LOGOUT))
            )
            return True
        except:
            return False

    def logout(self):
        button_logout = WebDriverWait(self.browser, 3).until(
            EC.visibility_of_element_located((AdminPageLocators.BUTTON_LOGOUT))
        )
        button_logout.click()

    def is_logged_out(self):
        try:
            WebDriverWait(self.browser, 3).until(
                EC.visibility_of_element_located((AdminPageLocators.INPUT_USER_NAME))
            )
            return True
        except:
            return False

    def navigate_to_product_catalog(self):
        """Переход в каталог продуктов."""
        self.wait_and_click(AdminPageLocators.CATALOG)
        self.wait_and_click(AdminPageLocators.PRODUCTS)

    def add_new_product(self, product_name):
        """Добавление нового продукта."""

        # Добавление продукта
        self.wait_and_click(AdminPageLocators.ADD_PRODUCT)

        # Ввод названия продукта
        self.wait_and_send_keys(AdminPageLocators.INPUT_PRODUCT_NAME, product_name)
        self.wait_and_send_keys(AdminPageLocators.INPUT_META_TAG_TITLE, product_name)

        # Переход на вкладку Data
        self.wait_and_click(AdminPageLocators.DATA_PRODUCT)
        self.wait_and_send_keys(AdminPageLocators.INPUT_MODEL, product_name)

        # Переход на вкладку SEO
        self.wait_and_click(AdminPageLocators.SEO_PRODUCT)
        self.wait_and_send_keys(AdminPageLocators.INPUT_SEO, product_name)

        # Сохранение продукта
        self.wait_and_click(AdminPageLocators.BUTTON_SAVE_PRODUCT)



    def search_product_added(self, product_name):
        """Поиск продукта."""
         #Попытка нажать кнопку "Назад", если она есть
        try:
                self.wait_and_click(AdminPageLocators.BUTTON_BACK)
        except TimeoutException:
            pass
            # Ввод названия продукта в фильтр
        self.wait_and_send_keys(AdminPageLocators.INPUT_FILTER_PRODUCT_NAME, product_name)
        # Нажатие кнопки "Фильтр"
        self.wait_and_click(AdminPageLocators.BUTTON_FILTER)
        # Получение текста карточки продукта
        product_text = self.wait_and_get_text(AdminPageLocators.PRODUCT_CARD)

        return product_text

    def delete_product(self):
        """Удаление продукта с подтверждением."""
        self.wait_and_click(AdminPageLocators.CHECK_BOX_CARD)
        self.wait_and_click(AdminPageLocators.BUTTON_DELETE_PRODUCT)
        alert = self.browser.switch_to.alert
        alert.accept()
