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
    service = Service('/Users/rohitwadi/PycharmProjects/OrangeHRM/chromedriver')
    driver = webdriver.Chrome(service=service)

    #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(driver_version="126.0.6478.62").install()))
    #chromedriver_autoinstaller.install()
    #driver = webdriver.Chrome()

    # service = Service(executable_path=ChromeDriverManager(driver_version="126.0.6478.126").install())
    # options = Options()
    # options.add_argument('--disable-blink-features=AutomationControlled')  ## to avoid getting detected
    # options.add_argument('headless')
    # options.add_argument('--disable-dev-shm-usage')
    # driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(15)
    driver.maximize_window()
    #yield
    #driver.quit()


@allure.description("Validate OrangeHRM with valid credentials")
@allure.severity(severity_level="CRITICAL")
def test_validLogin(test_setup):
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login");
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    log("Clicking Login Button")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    assert "dashboard" in driver.current_url


@allure.description("Validate OrangeHRM with invalid credentials")
@allure.severity(severity_level="NORMAL")
def test_invalidLogin(test_setup):
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login");
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("rohit123")
    log("Clicking login button")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    try:
        assert "dashboard" in driver.current_url
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