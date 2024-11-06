import pytest
from selenium import webdriver
from logger_config import logger


@pytest.fixture(scope="function")
def setup(request):
    logger.info("Запуск браузера")
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    request.cls.driver = driver
    yield driver
    driver.quit()
