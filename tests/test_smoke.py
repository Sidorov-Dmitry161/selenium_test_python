import time

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC

import pytest
from selenium.webdriver.support.wait import WebDriverWait

from pages.locators_page import *
from logger_config import logger

"""Авторизация"""
login = "standard_user"
password_all = "secret_sauce"

items = {
    1: "//button[@id='add-to-cart-sauce-labs-backpack']",
    2: "//button[@id='add-to-cart-sauce-labs-bike-light']",
    3: "//button[@id='add-to-cart-sauce-labs-bolt-t-shirt']",
    4: "//button[@id='add-to-cart-sauce-labs-fleece-jacket']",
    5: "//button[@id='add-to-cart-sauce-labs-onesie']",
    6: "//button[@id='add-to-cart-test.allthethings()-t-shirt-(red)']",
}

print("Приветствую тебя в нашем интернет магазине")


def get_user_input():
    while True:
        user_input = input("Выберете один из следующих товаров и укажите его номер через запятую: "
                           "1 - Sauce Labs Backpack \n"
                           "2 - Sauce Labs Bike Light \n"
                           "3 - Sauce Labs Bolt T-Shirt \n"
                           "4 - Sauce Labs Fleece Jacket \n"
                           "5 - Sauce Labs Onesie \n"
                           "6 - Sauce T-Shirt (Red) \n")
        selected_items = user_input.split(",")
        valid_items = []

        for item in selected_items:
            item = item.strip()
            if item.isdigit() and 1 <= int(item) <= 6:
                valid_items.append(int(item))  # Добавляем только валидные числа
            else:
                print("Пожалуйста, введите только цифры от 1 до 6 через запятую")
                break
        else:
            return valid_items  # Возвращаем список [...] валидных товаров


@pytest.mark.usefixtures("setup")
class TestSmoke:
    def test_login_page(self):
        logger.error("Тест начинается")

        # Получаем товары, которые выбрал пользователь
        get_item_from_user = get_user_input()
        print(f"Пользователь выбрал товары: {get_item_from_user}")

        """Логин"""
        login_pages = LoginPage(self.driver)
        login_pages.username_input(login)
        login_pages.password_input(password_all)
        login_pages.login_button()
        logger.info("Мы ввели логин и пароль")
        """Проверка что открылась нужная нам страница"""
        assert self.driver.find_element(By.XPATH, "//span[@class='title']").text == "Products", "Логин не удался"
        logger.info("Нужная страница открылась")

        """Добавляем выбранные товары в корзину"""
        # Перебираем номера товаров, выбранные пользователем
        for item_number in get_item_from_user:
            try:
                # Получаем XPath товара по его номеру
                item_xpath = items[item_number]
                logger.info(f"Ищем элемент с XPath: {item_xpath}")
                # Ожидаем, пока кнопка "Добавить в корзину" станет доступной, и нажимаем её
                add_to_cart_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, item_xpath))
                )
                add_to_cart_button.click()
                logger.info(f"Товар {item_number} добавлен в корзину")
            except Exception as e:
                logger.error(f"Ошибка при добавлении товара {item_number}: {e}")

        time.sleep(2)
        """Корзина"""
        cart_go = ItemPage(self.driver)
        cart_go.go_to_cart()
        logger.info("Кликнули на корзину")

        """Сравниваем товары и цены в корзине с выбранными пользователем"""
        # Названия всех товаров
        items_name = [
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Fleece Jacket",
            "Sauce Labs Onesie",
            "Test.allTheThings() T-Shirt (Red)"
        ]

        # Цены всех товаров
        items_price = [
            "$29.99",
            "$9.99",
            "$15.99",
            "$49.99",
            "$7.99",
            "$15.99"
        ]

        # Получаем товары, добавленные в корзину
        cart = Cart(self.driver)
        cart_item_names = cart.get_all_item_names()
        cart_item_prices = cart.get_all_item_prices()

        assert len(cart_item_names) == len(
            get_item_from_user), "Количество товаров в корзине не соответствует выбранным товарам"
        time.sleep(2)
        # Перебираем товары, которые выбрал пользователь, и сравниваем их с тем, что в корзине
        # Используем enumerate для получения индекса и значения
        for i, item_number in enumerate(get_item_from_user):
            expected_name = items_name[item_number - 1]
            expected_price = float(
                items_price[item_number - 1].replace("$", ""))  # Преобразуем цену в float для сравнения

            # Сравниваем название и цену каждого товара в корзине
            item_name_on_page = cart_item_names[i]  # Используем индекс i для списка товаров в корзине
            item_price_on_page = cart_item_prices[i]

            assert item_name_on_page == expected_name, f"Название товара {expected_name} не совпадает"
            assert item_price_on_page == expected_price, f"Цена товара {expected_price} не совпадает"

        """Прокрутка до 6-го товара, если пользователь выбрал все 6"""
        if len(get_item_from_user) == 6:
            # Прокручиваем к 6-му элементу, если он есть
            sixth_item_element = self.driver.find_element(By.XPATH, "//div[@class='cart_item'][6]")
            action = ActionChains(self.driver)
            action.move_to_element(sixth_item_element).perform()  # Прокручиваем к элементу

            # Определяем ожидаемое название и цену для 6-го товара
            expected_name = items_name[5]  # Индекс 5 для шестого элемента
            expected_price = float(items_price[5].replace("$", ""))  # Индекс 5 для шестого элемента

            # Получаем все названия и цены в корзине
            cart_item_names = cart.get_all_item_names()
            cart_item_prices = cart.get_all_item_prices()

            # Сравнение названия и цены 6-го товара
            sixth_item_name = cart_item_names[5]  # Получаем 6-й элемент из списка названий
            sixth_item_price = cart_item_prices[5]  # Получаем 6-й элемент из списка цен

            # Сравнение
            assert sixth_item_name == expected_name, "Название товара 6 не совпадает"
            assert sixth_item_price == expected_price, "Цена товара 6 не совпадает"

        time.sleep(1)
        # Нажимаем кнопку Checkout
        cart.btn_cart_checkout()

        # Вводим контактные данные юзера
        user_information = YourInformation(self.driver)
        user_information.first_name()
        user_information.last_name()
        user_information.zip_code()
        user_information.btn_continue()

        """Сравниваем цены товаров с итоговой суммой + налог"""
        checkout_page = CheckoutPage(self.driver)

        # Получаем цены всех товаров в корзине
        item_prices = checkout_page.get_item_prices()

        # Считаем итоговую сумму товаров
        calculated_item_total = sum(item_prices)

        # Сравниваем рассчитанную сумму товаров с тем, что отображается на странице
        item_total_on_page = checkout_page.get_item_total()
        assert calculated_item_total == item_total_on_page, (
            f"Ошибка: рассчитанная сумма товаров {calculated_item_total} не совпадает с суммой на странице {item_total_on_page}"
        )

        # Получаем налог
        tax_on_page = checkout_page.get_tax()

        # Рассчитываем ожидаемую общую сумму (Item total + Tax)
        expected_total = calculated_item_total + tax_on_page

        # Сравниваем общую сумму с отображаемым значением
        total_on_page = checkout_page.get_total()
        assert expected_total == total_on_page, (
            f"Ошибка: рассчитанная общая сумма {expected_total} не совпадает с суммой на странице {total_on_page}"
        )

        print("Проверка пройдена успешно: суммы товаров, налог и общая сумма совпадают.")
        checkout_page.bth_continue()

        finish = CompleteOrder(self.driver)
        check_out = finish.complete()
        assert check_out == "Thank you for your order!"
        print("Заказ успешно выполнен")
