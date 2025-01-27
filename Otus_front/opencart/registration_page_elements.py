from selenium.webdriver.common.by import By

class RegPageLocators:
    INPUT_FIRST_NAME = (By.ID, "input-firstname")
    INPUT_LAST_NAME = (By.ID, "input-lastname")
    INPUT_EMAIL = (By.ID, "input-email")
    INPUT_PASSWORD = (By.ID, "input-password")
    SWITCH_SUBSCRIBE = (By.ID, "input-newsletter")
    SWITSH_PRIVACY_POLICY = (By.NAME, "agree")
    BUTTON_REG = (By.XPATH, '//button[contains(text(), "Continue")]')
    COLUMN_RIGHT = (By.ID, "column-right")

