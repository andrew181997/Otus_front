from selenium.webdriver.common.by import By

class CardPageLocators:
    CONTAINER_PRODUCT = (By.ID, "product-info")
    PRODUCT_ICON = (By.XPATH, '//div[@class="image magnific-popup"]')
    PRICE_NEW = (By.CLASS_NAME, "price-new")
    TITLE_PRODUCT = (By.XPATH, '//h1[contains(text(), "Apple Cinema")]')
    ADD_TO_WISH_LIST = (By.XPATH, '//*[@formaction="http://192.168.0.102:8081/en-gb?route=account/wishlist.add"]')
    BUTTON_CART = (By.ID, "button-cart")