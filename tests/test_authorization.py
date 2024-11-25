import pytest
from logger_config import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.locators_page import LoginPage, Menu

password_all = "secret_sauce"
users = [
    ("standard_user", password_all, True),
    ("locked_out_user", password_all, False),
    ("problem_user", password_all, True),
    ("performance_glitch_user", password_all, True)
]


@pytest.mark.usefixtures("setup")
class TestAuthorization:

    def login(self, login, password):
        login_page = LoginPage(self.driver)
        login_page.username_input(login)
        login_page.password_input(password)
        login_page.login_button()
        logger.info(f"Логин и пароль введены для пользователя: {login}")

    def verify_successful_login(self):
        """Проверка успешного входа на страницу продуктов"""
        assert self.driver.find_element(By.XPATH, "//span[@class='title']").text == "Products", "Логин не удался"
        logger.info("Нужная страница открылась")

        menu = Menu(self.driver)
        menu.btn_menu()
        logger.info("Меню нажато")

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        )
        logger.info("Вход успешен, пользователь авторизован.")

    def verify_error_message(self, expected_message):
        """Проверка появления сообщения об ошибке"""
        error_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[@data-test='error']"))
        )
        assert expected_message in error_message.text, f"Ошибка: {error_message.text}"

    @pytest.mark.parametrize("username, password, is_successful", users)
    def test_login(self, username, password, is_successful):
        """Тест для различных типов пользователей"""
        self.login(username, password)

        if is_successful:
            self.verify_successful_login()
        else:
            self.verify_error_message("Epic sadface: Sorry, this user has been locked out.")
