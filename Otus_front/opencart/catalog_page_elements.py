from selenium.webdriver.common.by import By
url = "http://192.168.0.102:8081"
class CatalogPageLocators:
    LEFT_LIST = (By.ID, "column-left")
    BUTTON_HOME = (By.XPATH, '//a[@href="http://192.168.0.102:8081/en-gb?route=common/home"]')
    PLAYERS_IN_LEFT_LIST = (By.XPATH, '//a[contains(text(), "MP3 Players")]')
    PLAYERS_DOUGHTER= (By.XPATH, 'href="http://192.168.0.102:8081/en-gb/catalog/mp3-players/test-11"')
    pass
