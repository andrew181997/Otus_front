from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

class AdminPageLocators:
    LOGIN_FORM = (By.ID, "form-login")
    INPUT_USER_NAME = (By.ID, "input-username")
    INPUT_PASSWORD = (By.ID, "input-password")
    BUTTON_LOGIN = (By.XPATH, '//button[contains(text(), " Login")]')
    BUTTON_LOGOUT = (By.ID, "nav-logout")

class AdminPage:

    def __init__(self, browser):
        self.browser = browser

    def open_admin_page(self, url):
        self.browser.get(url)

    def login(self, username, password):
        input_user_name = WebDriverWait(self.browser, 3).until(
            EC.visibility_of_element_located(AdminPageLocators.INPUT_USER_NAME))
        input_password = WebDriverWait(self.browser, 3).until(
            EC.visibility_of_element_located(AdminPageLocators.INPUT_PASSWORD))

        button_login= WebDriverWait(self.browser, 3).until(
            EC.visibility_of_element_located(AdminPageLocators.BUTTON_LOGIN))
        input_user_name.send_keys(username)
        input_password.send_keys(password)
        button_login.click()

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