import pytest
from logger_config import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.locators_page import LoginPage, Menu

password_all = "secret_sauce"
standard_user = "standard_user"
locked_out_user = "locked_out_user"
problem_user = "problem_user"
performance_glitch_user = "performance_glitch_user"


@pytest.mark.usefixtures("setup")
class TestAuthorization:

    def login(self, login, password):
        login_page = LoginPage(self.driver)
        login_page.username_input(login)
        login_page.password_input(password)
        login_page.login_button()
        logger.info("Мы ввели логин и пароль")

    def test_login_standard_user(self):
        """Тест для стандартного пользователя"""
        self.login(standard_user, password_all)
        assert self.driver.find_element(By.XPATH, "//span[@class='title']").text == "Products", "Логин не удался"
        logger.info("Нужная страница открылась")

        menu = Menu(self.driver)
        menu.btn_menu()
        logger.info("Мы нажали на меню")

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        )
        logger.info(f"Вход успешен для пользователя: {standard_user}")

    def test_login_locked_out_user(self):
        """Тест для заблокированного пользователя"""
        self.login(locked_out_user, password_all)
        error_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[@data-test='error']"))
        )
        assert "Epic sadface: Sorry, this user has been locked out." in error_message.text

    def test_login_problem_user(self):
        """Тест для проблемного пользователя"""
        self.login(problem_user, password_all)
        assert self.driver.find_element(By.XPATH, "//span[@class='title']").text == "Products", "Логин не удался"
        logger.info("Нужная страница открылась")
        menu = Menu(self.driver)
        menu.btn_menu()
        logger.info("Мы нажали на меню")

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        )
        logger.info(f"Вход успешен для пользователя: {problem_user}")

    def test_login_performance_glitch_user(self):
        """Тест для пользователя с производственными проблемами"""
        self.login(performance_glitch_user, password_all)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='title']"))
        )
        assert self.driver.find_element(By.XPATH, "//span[@class='title']").text == "Products", "Логин не удался"
        logger.info("Нужная страница открылась")
        menu = Menu(self.driver)
        menu.btn_menu()
        logger.info("Мы нажали на меню")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        )
        logger.info(f"Вход успешен для пользователя: {performance_glitch_user}")
