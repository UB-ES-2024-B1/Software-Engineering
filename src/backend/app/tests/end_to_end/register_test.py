import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.crud import user_crud

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver_setup():
    # Define Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Example: Run in headless mode
    chrome_options.add_argument("--disable-gpu")

    # Initialize the WebDriver with options
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    """Setup the WebDriver and navigate to the app."""
    driver.get("http://localhost:8080/register")
    yield driver
    driver.quit()

@pytest.fixture
def db_session():
    """Set up a fresh database session for each test."""
    db: Session = SessionLocal()
    yield db
    db.close()

def test_register_success(driver_setup, db_session):
    driver = driver_setup
    
    # Fill the registration form
    driver.find_element(By.ID, "name").send_keys("Test User")
    driver.find_element(By.ID, "email").send_keys("testuser11@example.com")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "rePassword").send_keys("password123")
    
    # Submit the form
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)

    # Verify successful redirection to login
    assert "login" in driver.current_url, "Did not redirect to login after successful registration."

    # Now verify that the user exists in the database using the email
    created_user = user_crud.get_user_by_email(db_session, "testuser11@example.com")
    assert created_user is not None, "User was not created in the database."
    assert created_user.email == "testuser11@example.com", "The user's email does not match the expected email."
    user_crud.delete_user(db_session, created_user.id)

def test_register_mismatched_passwords(driver_setup):
    driver = driver_setup

    # Fill the registration form with mismatched passwords
    driver.find_element(By.ID, "name").send_keys("Test User")
    driver.find_element(By.ID, "email").send_keys("testuser12@example.com")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "rePassword").send_keys("password124")  # Mismatched password
    
    # Submit the form
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)

    # Verify that the error message for password mismatch appears
    password_error = driver.find_element(By.CSS_SELECTOR, ".error-message").text
    assert "Passwords do not match" in password_error, "Password mismatch error message did not appear."

def test_register_email_already_registered(driver_setup, db_session):
    driver = driver_setup

    # First, create a user with a known email in the database using the create_user function
    hashed_password = "password123"  # Use the plain password for simplicity
    created_user = user_crud.create_user(db_session, full_name="Existing User", email="testuser11@example.com", hashed_password=hashed_password)

    # Try to register with the same email
    driver.find_element(By.ID, "name").send_keys("Test User")
    driver.find_element(By.ID, "email").send_keys("testuser11@example.com")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "rePassword").send_keys("password123")

    # Submit the form
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)

    # Verify that the error message for already registered email appears
    email_error = driver.find_element(By.CSS_SELECTOR, ".error-message").text
    assert "Email already registered" in email_error, "Email already registered error message did not appear."

    user_crud.delete_user(db_session, created_user.id)

def test_register_empty_fields(driver_setup):
    driver = driver_setup

    # Submit the form with empty fields (name, email, and password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)

    # Verify that the required fields are empty
    name_field = driver.find_element(By.ID, "name")
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    
    assert name_field.get_attribute("value") == "", "Name field is not empty."
    assert email_field.get_attribute("value") == "", "Email field is not empty."
    assert password_field.get_attribute("value") == "", "Password field is not empty."
