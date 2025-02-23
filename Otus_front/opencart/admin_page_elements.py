import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from opencart.main_page import MainPage



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



class AdminPage(MainPage):


    def open_admin_page(self):
        self.logger.info("Открытие страницы администратора")
        self.browser.get("http://192.168.0.101:8081/administration")

    def login(self, username, password):
        self.logger.info("Попытка входа в админ-панель")
        self.wait_and_send_keys(AdminPageLocators.INPUT_USER_NAME, username)
        self.wait_and_send_keys(AdminPageLocators.INPUT_PASSWORD, password)
        self.wait_and_click(AdminPageLocators.BUTTON_LOGIN)
        self.logger.info("Авторизация выполнена")


    def is_logged_in(self):
        try:
            WebDriverWait(self.browser, 3).until(
                EC.visibility_of_element_located((AdminPageLocators.BUTTON_LOGOUT))
            )
            self.logger.info("Пользователь авторизован")
            return True
        except:
            return False

    def logout(self):
        self.logger.info("Выход из системы")
        button_logout = WebDriverWait(self.browser, 3).until(
            EC.visibility_of_element_located((AdminPageLocators.BUTTON_LOGOUT))
        )
        button_logout.click()

    def is_logged_out(self):

        try:
            WebDriverWait(self.browser, 3).until(
                EC.visibility_of_element_located((AdminPageLocators.INPUT_USER_NAME))
            )
            self.logger.info("Пользователь вышел из системы")
            return True
        except:
            return False

    def navigate_to_product_catalog(self):
        """Переход в каталог продуктов."""
        self.logger.info("Переход в каталог продуктов")
        self.wait_and_click(AdminPageLocators.CATALOG)
        self.wait_and_click(AdminPageLocators.PRODUCTS)

    def add_new_product(self, product_name):
        """Добавление нового продукта."""
        self.logger.info(f"Добавление нового продукта: {product_name}")
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
        self.wait_and_click(AdminPageLocators.BUTTON_SAVE_PRODUCT)
        self.logger.info("Продукт успешно добавлен")


    def search_product_added(self, product_name):
        """Поиск продукта."""
        self.logger.info(f"Поиск продукта: {product_name}")
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
        self.logger.info(f"Найден продукт с текстом: {product_text}")
        return product_text



    def delete_product(self):
        """Удаление продукта с подтверждением."""
        self.logger.info("Удаление продукта")
        self.wait_and_click(AdminPageLocators.CHECK_BOX_CARD)
        self.wait_and_click(AdminPageLocators.BUTTON_DELETE_PRODUCT)
        alert = self.browser.switch_to.alert
        alert.accept()
        input = self.browser.find_element(By.ID, 'input-name')
        input.clear()
        time.sleep(4)
        self.logger.info("Продукт успешно удален")

    def assert_text_not_visible(self, text, selector):
        """
        Проверяет, что указанный текст не отображается внутри элемента, найденного по селектору.

        :param text: Текст, который не должен отображаться.
        :param selector: Селектор элемента, в котором проверяется текст.
        """
        try:
            # Ожидаем, что текст не появится в элементе
            WebDriverWait(self.browser, 5).until_not(
                EC.text_to_be_present_in_element(selector, text)
            )
            time.sleep(4)
        except Exception as e:
            raise AssertionError(f"Текст '{text}' найден в элементе с селектором '{selector}'")