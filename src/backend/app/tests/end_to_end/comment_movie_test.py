import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.crud import movie_crud, user_crud, comments_crud
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

def test_comment_movie_success(login_user, db_session):
    driver = login_user
    # Navigate to the movie page
    driver.get("http://localhost:8080/movie/2")  # Change this URL to the movie page URL
    time.sleep(3)

    # Scroll to the comments section
    comments_section = driver.find_element(By.CLASS_NAME, "comments-section")
    driver.execute_script("arguments[0].scrollIntoView(true);", comments_section)
    time.sleep(2)  # Allow time for animation if any

    # Click the "New Comment" button
    new_comment_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "new-comment-btn"))
    )
    new_comment_btn.click()

    # Locate the text area and enter the comment
    comment_textarea = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "comment-textarea"))
    )
    comment_text = "This is a test comment."
    comment_textarea.send_keys(comment_text)

    # Post the comment
    post_comment_btn = driver.find_element(By.CLASS_NAME, "post-comment-btn")
    post_comment_btn.click()

    # Verify the comment is displayed
    added_comment = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'This is a test comment.')]"))
    )

    assert added_comment.is_displayed(), "The comment was not displayed correctly."
    
    # Verify the alert message is displayed
    alert_message_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "alert-modal"))
    )
    assert alert_message_element.is_displayed(), "The alert message was not displayed correctly."

    user = user_crud.get_user_by_email(db_session, "user2@example.com")
    thread = comments_crud.get_threads_by_movie(db_session, 2)
    comments = comments_crud.get_comments_by_thread(db_session, thread[0].id)
    
    matches = [m for m in comments if m.user_id == user.id and m.text == comment_text]

    # Check if any matches were found
    assert matches, f"No matching comment found for user_id={user.id} and text='{comment_text}'"

    # Delete the comment
    comments_crud.delete_comment(db_session, matches[0].id)

def test_delete_comment_movie_success(login_user, db_session):
    driver = login_user
    # Navigate to the movie page
    driver.get("http://localhost:8080/movie/3")  # Change this URL to the movie page URL
    time.sleep(3)
    
    # Scroll to the comments section
    comments_section = driver.find_element(By.CLASS_NAME, "comments-section")
    driver.execute_script("arguments[0].scrollIntoView(true);", comments_section)
    time.sleep(2)  # Allow time for animation if any

    # Click the "New Comment" button
    new_comment_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "new-comment-btn"))
    )
    new_comment_btn.click()

    # Locate the text area and enter the comment
    comment_textarea = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "comment-textarea"))
    )
    comment_text = "This is a test comment."
    comment_textarea.send_keys(comment_text)

    # Post the comment
    post_comment_btn = driver.find_element(By.CLASS_NAME, "post-comment-btn")
    post_comment_btn.click()
    

    # Verify the comment is displayed
    added_comment = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'This is a test comment.')]"))
    )

    assert added_comment.is_displayed(), "The comment was not displayed correctly."
    
    # Verify the alert message is displayed
    alert_message_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "alert-modal"))
    )
    assert alert_message_element.is_displayed(), "The alert message was not displayed correctly."

    yes_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "alert-close-btn"))
    )
    yes_button.click()

    user = user_crud.get_user_by_email(db_session, "user2@example.com")
    thread = comments_crud.get_threads_by_movie(db_session, 3)
    comments = comments_crud.get_comments_by_thread(db_session, thread[0].id)
    
    matches = [m for m in comments if m.user_id == user.id and m.text == comment_text]

    # Check if any matches were found
    assert matches, f"No matching comment found for user_id={user.id} and text='{comment_text}'"

    # Locate and click the "Delete Comment" button
    delete_comment_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "delete-comment-btn"))
    )
    delete_comment_btn.click()

    # Verify the confirmation modal (if present)
    confirmation_modal = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "delete-modal"))
    )
    assert confirmation_modal.is_displayed(), "The delete confirmation modal was not displayed."

    # Confirm deletion by clicking "Yes"
    confirm_delete_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Yes']"))
    )
    confirm_delete_btn.click()

    # Wait for the success message after deletion
    success_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "alert-modal"))
    )

    # Assert that the success message contains the expected text
    assert "The comment has been successfully deleted" in success_message.text, "The success message was not displayed correctly."


    comments = comments_crud.get_comments_by_thread(db_session, thread[0].id)
    
    matches = [m for m in comments if m.user_id == user.id and m.text == comment_text]

    # Check if any matches were found
    assert not matches, f"Found matching comment for user_id={user.id} and text='{comment_text}'"


def test_wishing_logged_out_user(driver_setup, db_session):
    driver = driver_setup
    # Navigate to the movie page without logging in
    driver.get("http://localhost:8080/movie/3")

    
    # Scroll to the comments section
    comments_section = driver.find_element(By.CLASS_NAME, "comments-section")
    driver.execute_script("arguments[0].scrollIntoView(true);", comments_section)
    time.sleep(2)  # Allow time for animation if any

    # Click the "New Comment" button
    new_comment_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "new-comment-btn"))
    )
    new_comment_btn.click()
   
    # Wait for the success message after deletion
    success_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "alert-modal"))
    )

    # Assert that the success message contains the expected text
    assert "You need to log in or register to access this feature." in success_message.text, "The alert message was not displayed correctly."



