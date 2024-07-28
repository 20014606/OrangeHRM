from pytest_bdd import scenario, scenarios, given, when, then
from pathlib import Path
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

from operations.test_login import log

featureFileDir ='features'
featureFile ='login.feature'
BASE_DIR = Path(__file__).resolve().parent
FEATURE_FILE = BASE_DIR.joinpath(featureFileDir).joinpath(featureFile)


@scenario(FEATURE_FILE, 'Successful login with valid credentials')
def test():
    print("end of test")
    pass


@given('I am on the login page')
def test_setup():
    global driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver = webdriver.Chrome()
    driver.implicitly_wait(20)
    driver.maximize_window()


@when('I enter a valid username and password')
def test_validLogin():
    driver.get("https://rohitwadi.pythonanywhere.com/")
    driver.find_element(By.XPATH, "//a[contains(text(), 'Login')]").click()
    driver.find_element(By.XPATH, "//input[@id='login_email']").clear()
    driver.find_element(By.XPATH, "//input[@id='login_password']").clear()
    driver.find_element(By.XPATH, "//input[@id='login_email']").send_keys("ro@gmail.com")
    driver.find_element(By.XPATH, "//input[@id='login_password']").send_keys("Daksh123")
    log("Clicking Login Button")
    driver.find_element(By.XPATH, "//input[@id='login_btn']").click()
    assert "FOOD ORDERING APP" in driver.page_source