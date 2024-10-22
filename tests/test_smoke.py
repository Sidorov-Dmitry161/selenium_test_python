import time

import pytest
from items_dict import items_dict


from pages.locators_page import *
from logger_config import logger

login = "standard_user"
password_all = "secret_sauce"


# Функция для получения ввода пользователя
def get_user_input():
    while True:
        user_input = input("Выберите один из следующих товаров и укажите его номер через запятую: "
                           "1 - Sauce Labs Backpack\n"
                           "2 - Sauce Labs Bike Light\n"
                           "3 - Sauce Labs Bolt T-Shirt\n"
                           "4 - Sauce Labs Fleece Jacket\n"
                           "5 - Sauce Labs Onesie\n"
                           "6 - Sauce T-Shirt (Red)\n")
        selected_items = user_input.split(",")
        valid_items = []
        for item in selected_items:
            item = item.strip()
            if item.isdigit() and 1 <= int(item) <= 6:
                valid_items.append(int(item))
            else:
                print("Пожалуйста, введите только цифры от 1 до 6 через запятую")
                break
        else:
            return valid_items


@pytest.mark.usefixtures("setup")
class TestSmoke:

    def test_login_page(self):
        logger.info("Тест начинается")

        # Получаем товары, которые выбрал пользователь
        get_item_from_user = get_user_input()
        print(f"Пользователь выбрал товары: {get_item_from_user}")

        # Логин
        login_pages = LoginPage(self.driver)
        login_pages.username_input(login)
        login_pages.password_input(password_all)
        login_pages.login_button()
        logger.info("Мы ввели логин и пароль")

        # Проверка, что открылась нужная нам страница
        assert self.driver.find_element(By.XPATH, "//span[@class='title']").text == "Products", "Логин не удался"
        logger.info("Нужная страница открылась")

        # Добавляем выбранные товары в корзину
        item_page = ItemPage(self.driver)
        for item_number in get_item_from_user:
            product_name = items_dict[item_number]
            try:
                logger.info(f"Добавляем товар {product_name} в корзину")
                item_page.add_to_cart(product_name)
                time.sleep(1)
            except Exception as e:
                logger.error(f"Ошибка при добавлении товара {product_name}: {e}")
        time.sleep(2)

        # Переход в корзину
        cart_page = Cart(self.driver)
        cart_page.go_to_cart()
        logger.info("Кликнули на корзину")
        cart_items = cart_page.get_cart_items()

        # Проверка, что выбранные пользователем товары находятся в корзине
        for item_number in get_item_from_user:
            expected_item_name = items_dict[item_number]
            assert expected_item_name in cart_items, f"Товар {expected_item_name} не был найден в корзине!"
        logger.info(f"Товары в корзине: {cart_items}")

        # Переход к оформлению заказа
        cart_page.proceed_to_checkout()

        # Вводим контактные данные пользователя
        user_information = YourInformation(self.driver)
        user_information.first_name()
        user_information.last_name()
        user_information.zip_code()
        user_information.btn_continue()

        # Сравниваем цены товаров с итоговой суммой и налогом
        checkout_page = CheckoutPage(self.driver)
        item_prices = checkout_page.get_item_prices()
        calculated_item_total = sum(item_prices)
        item_total_on_page = checkout_page.get_item_total()
        assert calculated_item_total == item_total_on_page, (
            f"Ошибка: рассчитанная сумма товаров {calculated_item_total} не совпадает с суммой на странице {item_total_on_page}"
        )
        tax_on_page = checkout_page.get_tax()
        expected_total = calculated_item_total + tax_on_page
        total_on_page = checkout_page.get_total()
        assert expected_total == total_on_page, (
            f"Ошибка: рассчитанная общая сумма {expected_total} не совпадает с суммой на странице {total_on_page}"
        )
        print("Проверка пройдена успешно: суммы товаров, налог и общая сумма совпадают.")

        # Завершение заказа
        checkout_page.btn_continue()
        finish = CompleteOrder(self.driver)
        check_out = finish.complete()
        assert check_out == "Thank you for your order!"
        print("Заказ успешно выполнен")
