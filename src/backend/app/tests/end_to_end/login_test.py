import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver_setup():
    """Setup the WebDriver and navigate to the login page."""
    # Define Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")    
    chrome_options.add_argument("--no-sandbox")
    
    # Initialize the WebDriver with options
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    # Navigate to the login page
    driver.get("http://localhost:8080/login")
    yield driver  # Provide the driver to the test
    driver.quit()  # Quit the driver after the test

def test_login_success(driver_setup):
    driver = driver_setup

    # Fill the login form
    driver.find_element(By.ID, "email").send_keys("user2@example.com")
    driver.find_element(By.ID, "password").send_keys("password2")
    
    # Submit the form
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)

    # Verify successful login redirection
    assert "/" in driver.current_url, "Login failed or did not redirect."

def test_login_invalid_credentials(driver_setup):
    driver = driver_setup

    # Attempt login with invalid credentials
    driver.find_element(By.ID, "email").send_keys("invalid@example.com")
    driver.find_element(By.ID, "password").send_keys("wrongpassword")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)

    # Verify error message is displayed
    error_message = driver.find_element(By.CLASS_NAME, "error-message").text
    assert "User not registered" in error_message, "Error message not shown for invalid credentials."
