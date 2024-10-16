from selenium.webdriver.common.by import By


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

    # Item 1
    def add_to_cart_item_1(self):
        btn_add_to_cart_1 = self.driver.find_element(By.XPATH, "//button[@id='add-to-cart-sauce-labs-backpack']")
        btn_add_to_cart_1.click()

    def get_item_1_text(self):
        return self.driver.find_element(By.XPATH, "//a[@id='item_4_title_link']").text

    def get_item_1_price(self):
        return self.driver.find_element(By.XPATH, "(//div[@class='inventory_item_price'])[1]").text

    # Item 2
    def add_to_cart_item_2(self):
        btn_add_to_cart_2 = self.driver.find_element(By.XPATH, "//button[@id='add-to-cart-sauce-labs-bike-light']")
        btn_add_to_cart_2.click()

    def get_item_2_text(self):
        return self.driver.find_element(By.XPATH, "//a[@id='item_0_title_link']").text

    def get_item_2_price(self):
        return self.driver.find_element(By.XPATH, "(//div[@class='inventory_item_price'])[2]")

    # Item 3
    def add_to_cart_item_3(self):
        btn_add_to_cart_3 = self.driver.find_element(By.XPATH, "//button[@id='add-to-cart-sauce-labs-bolt-t-shirt']")
        btn_add_to_cart_3.click()

    def get_item_3_text(self):
        return self.driver.find_element(By.XPATH, "//a[@id='item_1_title_link']").text

    def get_item_3_price(self):
        return self.driver.find_element(By.XPATH, "(//div[@class='inventory_item_price'])[3]")

    # Item 4
    def add_to_cart_item_4(self):
        btn_add_to_cart_4 = self.driver.find_element(By.XPATH, "//button[@id='add-to-cart-sauce-labs-fleece-jacket']")
        btn_add_to_cart_4.click()

    def get_item_4_text(self):
        return self.driver.find_element(By.XPATH, "//a[@id='item_5_title_link']")

    def get_item_4_price(self):
        return self.driver.find_element(By.XPATH, "(//div[@class='inventory_item_price'])[4]")

    # Item 5
    def add_to_cart_item_5(self):
        btn_add_to_cart_5 = self.driver.find_element(By.XPATH, "//button[@id='add-to-cart-sauce-labs-onesie']")
        btn_add_to_cart_5.click()

    def get_item_5_text(self):
        return self.driver.find_element(By.XPATH, "//a[@id='item_2_title_link']")

    def get_item_5_price(self):
        return self.driver.find_element(By.XPATH, "(//div[@class='inventory_item_price'])[5]")

    # Item 6
    def add_to_cart_item_6(self):
        btn_add_to_cart_6 = self.driver.find_element(By.XPATH,
                                                     "//button[@id='add-to-cart-test.allthethings()-t-shirt-(red)']")
        btn_add_to_cart_6.click()

    def get_item_6_text(self):
        return self.driver.find_element(By.XPATH, "//a[@id='item_3_title_link']")

    def get_item_6_price(self):
        return self.driver.find_element(By.XPATH, "(//div[@class='inventory_item_price'])[6]")

    def go_to_cart(self):
        cart = self.driver.find_element(By.XPATH, "//*[@id='shopping_cart_container']/a")
        cart.click()


class Cart:
    def __init__(self, driver):
        self.driver = driver

    def get_cart_items(self):
        # Находим все элементы с названиями товаров в корзине
        names = self.driver.find_elements(By.XPATH, "//div[@class='inventory_item_name']")
        # Находим все элементы с ценами товаров в корзине
        prices = self.driver.find_elements(By.XPATH, "//div[@class='inventory_item_price']")

        # Создаём пустой словарь для хранения названий товаров и их цен
        cart_items = {}

        # Используем zip, чтобы одновременно пройтись по названиям и ценам
        for name, price in zip(names, prices):
            cart_items[name.text] = float(price.text.replace("$", ""))

        return cart_items

    def get_all_item_names(self):
        # Находим все элементы с товарами по XPATH
        items = self.driver.find_elements(By.XPATH, "//a[contains(@id, 'item_') and contains(@id, '_title_link')]")
        # Возвращаем список названий товаров (текстовое содержание каждого элемента)
        return [item.text for item in items]

    def get_all_item_prices(self):
        # Находим все элементы, содержащие цены товаров по XPATH
        prices = self.driver.find_elements(By.XPATH, "//div[@class='inventory_item_price']")
        # Возвращаем список цен, преобразованных в float, удаляя знак "$"
        return [float(price.text.replace("$", "")) for price in prices]

    def btn_cart_checkout(self):
        cart_checkout = self.driver.find_element(By.XPATH, "//button[@id='checkout']")
        cart_checkout.click()


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
    # Локаторы для элементов на странице
    ITEM_TOTAL = (By.XPATH, "//div[@class='summary_subtotal_label']")
    TAX = (By.XPATH, "//div[@class='summary_tax_label']")
    TOTAL = (By.XPATH, "//div[@class='summary_total_label']")
    ITEM_PRICES = (By.XPATH, "//div[@class='inventory_item_price']")  # Все цены товаров в корзине

    def __init__(self, driver):
        self.driver = driver

    # Получаем цены всех товаров в корзине и возвращаем их в виде списка
    def get_item_prices(self):
        prices_elements = self.driver.find_elements(*CheckoutPage.ITEM_PRICES)
        # Преобразуем текстовое значение каждой цены в float и возвращаем список цен
        return [float(price.text.replace("$", "")) for price in prices_elements]

    # Получаем итоговую сумму товаров (Item total)
    def get_item_total(self):
        item_total_text = self.driver.find_element(*CheckoutPage.ITEM_TOTAL).text
        # Извлекаем числовое значение из текста и преобразуем его в float
        return float(item_total_text.replace("Item total: $", ""))

    # Получаем налог
    def get_tax(self):
        tax_text = self.driver.find_element(*CheckoutPage.TAX).text
        # Извлекаем числовое значение из текста налога и преобразуем его в float
        return float(tax_text.replace("Tax: $", ""))

    # Получаем общую сумму (Total)
    def get_total(self):
        total_text = self.driver.find_element(*CheckoutPage.TOTAL).text
        # Извлекаем числовое значение общей суммы и преобразуем его в float
        return float(total_text.replace("Total: $", ""))

    def bth_continue(self):
        btn_continue = self.driver.find_element(By.ID, "finish")
        btn_continue.click()


class CompleteOrder:
    def __init__(self, driver):
        self.driver = driver

    def complete(self):
        complete = self.driver.find_element(By.CLASS_NAME, 'complete-header')
        return complete.text
