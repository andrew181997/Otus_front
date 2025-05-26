from selenium.webdriver.common.by import By
from .admin_page_elements import AdminPage
import uuid
class RegPageLocators:
    INPUT_FIRST_NAME = (By.ID, "input-firstname")
    INPUT_LAST_NAME = (By.ID, "input-lastname")
    INPUT_EMAIL = (By.ID, "input-email")
    INPUT_PASSWORD = (By.ID, "input-password")
    SWITCH_SUBSCRIBE = (By.ID, "input-newsletter")
    SWITSH_PRIVACY_POLICY = (By.NAME, "agree")
    BUTTON_REG = (By.XPATH, '//button[contains(text(), "Continue")]')
    COLUMN_RIGHT = (By.ID, "column-right")
    CHECK_REGISTRATION_BANNER = (By.TAG_NAME, "h1")
url = "http://192.168.0.102:8081"
class RegPage(AdminPage):
    url = "http://192.168.0.102:8081"
    def open_page_registartion(self):
        self.browser.get(f"{url}/en-gb?route=account/register")

    def rigistration_member(self):
        self.wait_and_send_keys(RegPageLocators.INPUT_FIRST_NAME, "Andrew")
        self.wait_and_send_keys(RegPageLocators.INPUT_EMAIL, f"{uuid.uuid4()}@yandex.ru")
        self.wait_and_send_keys(RegPageLocators.INPUT_LAST_NAME, "Demidov")
        self.wait_and_send_keys(RegPageLocators.INPUT_PASSWORD, "Andrew")
        self.wait_and_click(RegPageLocators.SWITSH_PRIVACY_POLICY)
        self.wait_and_click(RegPageLocators.BUTTON_REG)



