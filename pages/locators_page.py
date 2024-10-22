from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logger_config import logger


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def username_input(self, username):
        username_field = self.driver.find_element(By.ID, "user-name")
        username_field.clear()
        username_field.send_keys(username)

    def password_input(self, password):
        password_field = self.driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)

    def login_button(self):
        login_btn = self.driver.find_element(By.ID, "login-button")
        login_btn.click()


class ItemPage:
    def __init__(self, driver):
        self.driver = driver

    def add_to_cart(self, product_name):
        try:
            add_to_cart_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            f"//button[contains(@data-test, 'add-to-cart-{product_name.lower().replace(' ', '-')}')]"))
            )
            add_to_cart_button.click()
            logger.info(f"Товар {product_name} добавлен в корзину успешно!")
            return True
        except Exception as e:
            logger.error(f"Ошибка при добавлении товара {product_name}: {e}")
            return False


class Cart:
    def __init__(self, driver):
        self.driver = driver

    def get_cart_items(self):
        item_elements = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        cart_items = [item.text for item in item_elements]
        print(f"Товары в корзине: {cart_items}")
        return cart_items

    def proceed_to_checkout(self):
        self.driver.find_element(By.ID, "checkout").click()

    def go_to_cart(self):
        cart = self.driver.find_element(By.XPATH, "//*[@id='shopping_cart_container']/a")
        cart.click()


class YourInformation:
    def __init__(self, driver):
        self.driver = driver

    def first_name(self):
        first_name = self.driver.find_element(By.ID, "first-name")
        first_name.send_keys("Ivan")

    def last_name(self):
        last_name = self.driver.find_element(By.ID, "last-name")
        last_name.send_keys("Ivanov")

    def zip_code(self):
        zip_code = self.driver.find_element(By.ID, "postal-code")
        zip_code.send_keys("3405")

    def btn_continue(self):
        btn_continue = self.driver.find_element(By.ID, "continue")
        btn_continue.click()


class CheckoutPage:
    ITEM_TOTAL = (By.XPATH, "//div[@class='summary_subtotal_label']")
    TAX = (By.XPATH, "//div[@class='summary_tax_label']")
    TOTAL = (By.XPATH, "//div[@class='summary_total_label']")
    ITEM_PRICES = (By.XPATH, "//div[@class='inventory_item_price']")

    def __init__(self, driver):
        self.driver = driver

    def get_item_prices(self):
        prices_elements = self.driver.find_elements(*CheckoutPage.ITEM_PRICES)
        return [float(price.text.replace("$", "")) for price in prices_elements]

    def get_item_total(self):
        item_total_text = self.driver.find_element(*CheckoutPage.ITEM_TOTAL).text
        return float(item_total_text.replace("Item total: $", ""))

    def get_tax(self):
        tax_text = self.driver.find_element(*CheckoutPage.TAX).text
        return float(tax_text.replace("Tax: $", ""))

    def get_total(self):
        total_text = self.driver.find_element(*CheckoutPage.TOTAL).text
        return float(total_text.replace("Total: $", ""))

    def btn_continue(self):
        btn_continue = self.driver.find_element(By.ID, "finish")
        btn_continue.click()


class CompleteOrder:
    def __init__(self, driver):
        self.driver = driver

    def complete(self):
        complete = self.driver.find_element(By.CLASS_NAME, 'complete-header')
        return complete.text
