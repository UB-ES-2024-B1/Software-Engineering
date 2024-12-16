import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.crud import movie_crud, user_crud
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
@pytest.fixture
def driver_setup():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    driver.get("http://localhost:8080/login")
    yield driver
    driver.quit()

@pytest.fixture
def db_session():
    db: Session = SessionLocal()
    yield db
    db.close()

@pytest.fixture
def login_user(driver_setup, db_session):
    """Helper fixture to log in a user."""
    # Assume login is possible with email and password
    driver = driver_setup
    driver.find_element(By.ID, "email").send_keys("user2@example.com")
    driver.find_element(By.ID, "password").send_keys("password2")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)  # Wait for the page to load after login
    return driver


def test_toggle_premium_button_for_logged_in_user(login_user, db_session):
    driver = login_user

    # Navigate to the page containing the button
    driver.get("http://localhost:8080")  # Replace with the appropriate URL
    time.sleep(3)

    # Find the Premium button in the header
    premium_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.Btn"))
    )
    
    # Initial state check (before any click)
    initial_button_class = premium_button.get_attribute("class")
    assert "premium-button" in initial_button_class, "The button should be in premium mode initially."

    '''user = user_crud.get_user_by_email(db_session, "user2@example.com")
    print(user)
    assert user.is_premium, "User is not initialy premium"
    '''
    # Click the button to open the downgrade modal
    premium_button.click()
    time.sleep(2)

    # Verify the Downgrade modal appears (since the user is premium)
    downgrade_modal = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-overlay h2"))
    )
    assert "Premium Downgrade" in downgrade_modal.text, "Downgrade modal did not appear."

    # Click the "Downgrade" button to confirm downgrade
    downgrade_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Downgrade')]")
    downgrade_button.click()
    time.sleep(2)

    # Verify the Downgrade confirmation modal and click the "Ok" button
    downgrade_confirmation_modal = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-overlay h2"))
    )
    assert "Premium Downgrade" in downgrade_confirmation_modal.text, "Downgrade confirmation modal did not appear."
    ok_button = driver.find_element(By.CSS_SELECTOR, ".modal-buttons button.ok-button")
    ok_button.click()
    time.sleep(2)

    
    final_button_class = premium_button.get_attribute("class")
    assert "premium-button" not in final_button_class, "The button did not toggle state as expected."

    '''user = user_crud.get_user_by_email(db_session, "user2@example.com")
    print(user)
    assert not user.is_premium, "User did not change to non premium in database"
    '''
    # Click the Premium button again to open the upgrade modal
    premium_button.click()
    time.sleep(2)

    # Verify the Upgrade modal appears (for the downgrade state)
    upgrade_modal = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-overlay h2"))
    )
    assert "UPGRADE TO PREMIUM" in upgrade_modal.text, "Upgrade modal did not appear."

    # Click the "Upgrade" button to confirm the upgrade
    upgrade_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Upgrade')]")
    upgrade_button.click()
    time.sleep(2)

    # Verify the Upgrade confirmation modal and click the "Ok" button
    upgrade_confirmation_modal = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-overlay h2"))
    )
    assert "Premium Upgrade" in upgrade_confirmation_modal.text, "Upgrade confirmation modal did not appear."
    ok_button = driver.find_element(By.CSS_SELECTOR, ".modal-buttons button.ok-button")
    ok_button.click()
    time.sleep(2)

    # Check that the button class has toggled back to non-premium state (after upgrade)
    final_button_class = premium_button.get_attribute("class")
    assert "premium-button" in final_button_class, "The button did not toggle state as expected."

    '''user = user_crud.get_user_by_email(db_session, "user2@example.com")
    assert user.is_premium, "User is not premium in database"'''

def test_create_new_list_success(login_user, db_session):
    driver = login_user
    
    # Navigate to the profile page 
    driver.get("http://localhost:8080/profile")
    time.sleep(3)
    
    # Click the "Add New" button
    add_new_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "add-new-list-btn"))
    )
    add_new_button.click()
    time.sleep(2)
    
    # Wait for the modal to appear
    modal = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "modal-content"))
    )
    assert modal.is_displayed(), "Modal did not appear after clicking 'Add New' button."

    # Enter the list name
    list_name_input = driver.find_element(By.ID, "list-name")
    list_name = "My Test List"  
    list_name_input.send_keys(list_name)
    
    # Click the "Create List" button
    create_button = driver.find_element(By.CLASS_NAME, "create-btn")
    create_button.click()
    time.sleep(3)
    
    # Verify the new list button appears in the dynamic-buttons section
    new_list_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//button[contains(text(), '{list_name}')]"))
    )
    assert new_list_button.is_displayed(), f"New list '{list_name}' was not created successfully."
        
        
    list = user_crud.get_list_type_by_name(db_session, list_name,"user2@example.com")
    assert list.name == "My Test List", f"New list '{list_name}' was not created successfully in backend."

    # Remove the test list
    delete_button = new_list_button.find_element(By.CLASS_NAME, "delete-button-list")
    delete_button.click()
    
    delete_confirm_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "create-btn"))
    )
    delete_confirm_button.click()
    time.sleep(3)

    # Verify the list is removed
    deleted_list = driver.find_elements(By.XPATH, f"//button[contains(text(), '{list_name}')]")
    assert len(deleted_list) == 0, f"List '{list_name}' was not deleted after cleanup."

    list_lists = user_crud.get_user_lists_by_email(db_session,"user2@example.com")
    assert all(l.name != list_name for l in list_lists), f"List '{list_name}' was not deleted after cleanup from backend."

def test_add_movie_new_list_success(login_user, db_session):
    driver = login_user

    # Navigate to the profile page
    driver.get("http://localhost:8080/profile")
    time.sleep(3)

    # Click the "Add New" button
    add_new_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "add-new-list-btn"))
    )
    add_new_button.click()
    time.sleep(2)

    # Wait for the modal to appear
    modal = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "modal-content"))
    )
    assert modal.is_displayed(), "Modal did not appear after clicking 'Add New' button."

    # Enter the list name
    list_name_input = driver.find_element(By.ID, "list-name")
    list_name = "My Test List"
    list_name_input.send_keys(list_name)

    # Click the "Create List" button
    create_button = driver.find_element(By.CLASS_NAME, "create-btn")
    create_button.click()
    time.sleep(3)

    # Verify the new list button appears in the dynamic-buttons section
    new_list_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//button[contains(text(), '{list_name}')]"))
    )
    assert new_list_button.is_displayed(), f"New list '{list_name}' was not created successfully."

    # Verify the backend entry
    list = user_crud.get_list_type_by_name(db_session, list_name, "user2@example.com")
    assert list.name == "My Test List", f"New list '{list_name}' was not created successfully in backend."

    # Navigate to the movie page
    driver.get("http://localhost:8080/movie/10")
    time.sleep(3)

    
    # Click the "Add to List" button (plusButton)
    plus_buttons = WebDriverWait(driver, 10).until(
    lambda d: d.find_elements(By.CLASS_NAME, "plusButton")
    )

    # Select the second plusButton
    add_to_list_button = plus_buttons[1]
    add_to_list_button.click()
    time.sleep(2)

    # Verify the modal for selecting lists appears
    select_list_modal = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "modal-content"))
    )
    assert select_list_modal.is_displayed(), "Modal to select a list did not appear."

    # Click the "Add" button for the specific list in the modal
    add_to_specific_list_button = driver.find_element(
        By.XPATH, f"//span[contains(text(), '{list_name}')]/following-sibling::button"
    )
    add_to_specific_list_button.click()
    time.sleep(3)

    list_lists = user_crud.get_list_type_by_name(db_session, list_name, "user2@example.com")
    movie_added = movie_crud.get_movie(db_session, 10)
    assert any(movie.movie.title == movie_added.title for movie in list_lists.movies), f"Movie {movie_added.title} was not created successfully in backend."

    # Navigate back to the profile page
    driver.get("http://localhost:8080/profile")
    time.sleep(3)

    # Verify the new list button appears in the dynamic-buttons section
    new_list_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//button[contains(text(), '{list_name}')]"))
    )

    # Hover over the new list button to make the delete button visible
    actions = ActionChains(driver)
    actions.move_to_element(new_list_button).perform()  # Hover over the new list button
    time.sleep(1)  

    # Remove the test list
    delete_button = new_list_button.find_element(By.CLASS_NAME, "delete-button-list")
    delete_button.click()

    delete_confirm_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "create-btn"))
    )
    delete_confirm_button.click()
    time.sleep(3)

    # Verify the list is removed
    deleted_list = driver.find_elements(By.XPATH, f"//button[contains(text(), '{list_name}')]")
    assert len(deleted_list) == 0, f"List '{list_name}' was not deleted after cleanup."

    # Verify backend list deletion
    list_lists = user_crud.get_user_lists_by_email(db_session, "user2@example.com")
    assert all(l.name != list_name for l in list_lists), f"List '{list_name}' was not deleted from the backend after cleanup."

    list_lists = user_crud.get_user_lists_by_email(db_session,"user2@example.com")
    assert all(l.name != list_name for l in list_lists), f"List '{list_name}' was not deleted after cleanup from backend."
