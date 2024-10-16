import pytest
from selenium import webdriver
from logger_config import logger


@pytest.fixture(scope="class")
def setup(request):
    logger.info("Запуск браузера")
    driver = webdriver.Chrome()  # или другой драйвер, если ты используешь другой браузер
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.quit()
