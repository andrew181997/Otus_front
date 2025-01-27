from selenium.webdriver.common.by import By

class MainPageLocators:
    CART_ICON = (By.CLASS_NAME, "fa-cart-shopping")
    LOGO = (By.ID, "logo")
    MENU = (By.ID, "narbar-menu")
    FOOTER = (By.TAG_NAME, "footer")
    CAROUSEL_BANNER = (By.ID, "carousel-banner-1")
    SEARCH = (By.ID, "search")