from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Конфигурация
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
FIRST_NAME = "Евгений"
LAST_NAME = "Иванов"
ZIP_CODE = "241047"
BASE_URL = "https://www.saucedemo.com/"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

def add_product_to_cart(product_id, product_name_xpath, price_xpath, add_to_cart_xpath):
    product_name = driver.find_element(By.XPATH, product_name_xpath).text
    product_price = driver.find_element(By.XPATH, price_xpath).text
    driver.find_element(By.XPATH, add_to_cart_xpath).click()
    logging.info(f"Товар {product_name} добавлен в корзину")
    return product_name, product_price

# Указываем путь к chromedriver через объект Service
service = Service("/usr/bin/chromedriver")

# Используем контекстный менеджер для управления драйвером
with webdriver.Chrome(service=service) as driver:
    driver.get(BASE_URL)
    logging.info("Страница открыта")

    # Авторизация на сайте
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='user-name']"))).send_keys(USERNAME)
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//input[@id='login-button']").click()
    logging.info("Успешная авторизация")

    # Добавление товаров в корзину
    product_1_name, product_1_price = add_product_to_cart(
        "item_4_title_link", 
        "//a[@id='item_4_title_link']", 
        "(//div[@class='inventory_item_price'])[1]", 
        "//button[@id='add-to-cart-sauce-labs-backpack']"
    )

    product_2_name, product_2_price = add_product_to_cart(
        "item_0_title_link", 
        "//a[@id='item_0_title_link']", 
        "(//div[@class='inventory_item_price'])[2]", 
        "//button[@id='add-to-cart-sauce-labs-bike-light']"
    )

    # Переход в корзину
    driver.find_element(By.XPATH, "//a[@class='shopping_cart_link']").click()
    logging.info("Переход в корзину")

    # Проверка товаров в корзине
    cart_product_1_name = driver.find_element(By.XPATH, "//a[@id='item_4_title_link']").text
    assert product_1_name == cart_product_1_name
    logging.info("Название первого продукта верно")

    cart_product_2_name = driver.find_element(By.XPATH, "//a[@id='item_0_title_link']").text
    assert product_2_name == cart_product_2_name
    logging.info("Название второго продукта верно")

    # Оформление заказа
    driver.find_element(By.XPATH, "//button[@id='checkout']").click()
    logging.info("Нажали checkout")

    # Ввод данных пользователя
    driver.find_element(By.XPATH, "//input[@id='first-name']").send_keys(FIRST_NAME)
    driver.find_element(By.XPATH, "//input[@id='last-name']").send_keys(LAST_NAME)
    driver.find_element(By.XPATH, "//input[@id='postal-code']").send_keys(ZIP_CODE)
    driver.find_element(By.XPATH, "//input[@id='continue']").click()
    logging.info("Данные пользователя введены")

    # Проверка итоговой информации
    finish_product_1_name = driver.find_element(By.XPATH, "//a[@id='item_4_title_link']").text
    assert product_1_name == finish_product_1_name
    logging.info("Конечное название первого продукта верно")

    finish_product_2_name = driver.find_element(By.XPATH, "//a[@id='item_0_title_link']").text
    assert product_2_name == finish_product_2_name
    logging.info("Конечное название второго продукта верно")

    # Завершение заказа
    driver.find_element(By.XPATH, "//button[@id='finish']").click()
    logging.info("Заказ завершен")
