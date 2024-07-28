import time

import pytest
from selenium import webdriver
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

@pytest.fixture()
def test_setup():
    global driver
    #driver = webdriver.Chrome(executable_path="/Users/rohitwadi/PycharmProjects/OrangeHRM/chromedriver")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    #chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()

    # service = Service(executable_path=ChromeDriverManager(latest_release_url='https://chromedriver.storage.googleapis.com/113.0.5672.63/chromedriver_mac_arm64.zip', driver_version="113.0.5672.63").install())
    # options = Options()
    # options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument('headless')
    # options.add_argument('--disable-dev-shm-usage')
    # driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(20)
    driver.maximize_window()
    #yield
    #driver.quit()


@allure.description("Validate FoodOrderingApp with valid credentials")
@allure.severity(severity_level="CRITICAL")
def test_validLogin(test_setup):
    driver.get("https://rohitwadi.pythonanywhere.com/")
    driver.find_element(By.XPATH, "//a[contains(text(), 'Login')]").click()
    driver.find_element(By.XPATH, "//input[@id='login_email']").clear()
    driver.find_element(By.XPATH, "//input[@id='login_password']").clear()
    driver.find_element(By.XPATH, "//input[@id='login_email']").send_keys("ro@gmail.com")
    driver.find_element(By.XPATH, "//input[@id='login_password']").send_keys("Daksh123")
    log("Clicking Login Button")
    driver.find_element(By.XPATH, "//input[@id='login_btn']").click()
    assert "FOOD ORDERING APP" in driver.page_source


@allure.description("Validate FoodOrderingApp with invalid credentials")
@allure.severity(severity_level="NORMAL")
def test_invalidLogin(test_setup):
    driver.get("https://rohitwadi.pythonanywhere.com/")
    driver.find_element(By.XPATH, "//a[contains(text(), 'Login')]").click()
    driver.find_element(By.XPATH, "//input[@id='login_email']").clear()
    driver.find_element(By.XPATH, "//input[@id='login_password']").clear()
    driver.find_element(By.XPATH, "//input[@id='login_email']").send_keys("ro@gmail.com")
    driver.find_element(By.XPATH, "//input[@id='login_password']").send_keys("rohit123")
    log("Clicking Login Button")
    driver.find_element(By.XPATH, "//input[@id='login_btn']").click()
    try:
        assert "All Restaurants" in driver.page_source
    finally:
        if AssertionError:
            time.sleep(15)
            allure.attach(driver.get_screenshot_as_png(),
                          name="Invalid Credentials",
                          attachment_type=allure.attachment_type.PNG)


@allure.step("Entering Username as {0}")
def enter_username(username):
    driver.find_element(By.NAME, "username").send_keys(username);


@allure.step("Entering Password as {0}")
def enter_password(password):
    driver.find_element(By.NAME, "password").send_keys(password)


@allure.step("{0}")
def log(message):
    print(message)


@pytest.fixture()
def test_teardown():
    driver.quit()