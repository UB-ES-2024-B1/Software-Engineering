import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.crud import movie_crud, user_crud, comments_crud
from app.models.comments_model import ReportStatus

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
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)  # Wait for the page to load after login
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


def test_comment_logged_out_user(driver_setup, db_session):
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



def test_report_comment_success(login_user, db_session):
    driver = login_user

    # Navigate to the movie page
    driver.get("http://localhost:8080/movie/3")  # Change this URL to the correct movie page URL
    time.sleep(3)

    # Scroll to the comments section
    comments_section = driver.find_element(By.CLASS_NAME, "comments-section")
    driver.execute_script("arguments[0].scrollIntoView(true);", comments_section)
    time.sleep(3)  # Allow time for animation if any

    # Identify the comment you want to report (you can choose any comment here, like the first one)
    comment = driver.find_element(By.CSS_SELECTOR, ".comment-item p")  # Modify the selector if needed
    comment_text_user = comment.text  # Get the text of the comment

    # Identify a comment that can be reported
    report_comment_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "report-comment-btn"))
    )
    time.sleep(3)
    
    # Click the "Report Comment" button
    report_comment_btn.click()
    # Verify the report confirmation modal is displayed
    report_modal = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "report-modal"))
    )
    assert report_modal.is_displayed(), "The report confirmation modal was not displayed."

    # Confirm the report
    confirm_report_btn = driver.find_element(By.XPATH, "//button[text()='Yes']")
    confirm_report_btn.click()

    # Wait for the success message after reported
    success_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "alert-modal"))
    )

    # Assert that the success message contains the expected text
    assert "Comment reported successfully." in success_message.text, "The success message was not displayed correctly."

    # Close the success alert
    alert_close_btn = driver.find_element(By.CLASS_NAME, "alert-close-btn")
    alert_close_btn.click()

    # Validate in the database if the comment was reported
    user = user_crud.get_user_by_email(db_session, "user2@example.com")
    thread = comments_crud.get_threads_by_movie(db_session, 3)
    comments = comments_crud.get_comments_by_thread(db_session, thread[0].id)
    comments_reported = comments_crud.get_comments_reported_by_user(db_session, user.id)
    
    comment_ids = {comment.id for comment in comments}
    reported_comment_ids = {reported_comment.id for reported_comment in comments_reported}

    # Find the intersection of the two sets
    common_ids = comment_ids & reported_comment_ids

    # Assert that at least one comment is reported
    assert common_ids, "No comments in the thread are reported by the user"

    driver.get("http://localhost:8080/profile")
    time.sleep(2)

    # Verify that the user was redirected to the profile page
    assert "profile" in driver.current_url, "User was not redirected to profile page."
    
    # Wait for the profile page to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "profile-page"))
    )

    # Identify a comment that can be reported
    report_comment_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "report-comments-btn"))
    )
    time.sleep(3)

    report_comment_btn.click()
    
    time.sleep(2)
    
    # Verify that the user was redirected to the profile page
    assert "reportedComments" in driver.current_url, "User was not redirected to reportedComments page."

    
    # Wait for the reported comments list to load
    reported_comments_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "scrollable-comments-admin"))
    )

    # Retrieve all reported comments visible on the page
    reported_comments = driver.find_elements(By.CLASS_NAME, "scrollable-comments-admin")

    # Assert that at least one comment is visible
    assert len(reported_comments) > 0, "No reported comments are displayed on the page."

    # Verify that the reported comment is present by checking its text
    reported_comment_texts = [comment.find_element(By.CSS_SELECTOR, ".comment-link p").text for comment in reported_comments]

    # Assert that the reported comment text is displayed on the page
    assert any(comment_text == comment_text_user for comment_text in reported_comment_texts), \
        f"The reported comment '{comment_text_user}' is not displayed on the page."

    # Iterate over each reported comment
    for reported_comment in reported_comments:
        # Get the text of the comment for verification
        reported_comment_text = reported_comment.find_element(By.CSS_SELECTOR, ".comment-link p").text

        # Check if this is the reported comment we want to clear
        if reported_comment_text == comment_text_user:  # Match with the text of the reported comment
            # Click the dropdown to select a new state
            dropdown_button = reported_comment.find_element(By.CLASS_NAME, "dropdown-button-reported")
            dropdown_button.click()

            # Wait for the dropdown menu to appear
            WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "dropdown-menu"))
            )

            # Find and click the "CLEAN" option in the dropdown menu
            clear_option = driver.find_element(By.XPATH, "//li[text()='CLEAN']")
            clear_option.click()

            # Optionally, handle confirmation modal if needed
            confirmation_modal = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "confirmation-modal"))
            )
            confirm_clear_btn = confirmation_modal.find_element(By.CLASS_NAME, "confirm-btn")
            confirm_clear_btn.click()

            # Handle the alert and check the text
            WebDriverWait(driver, 20).until(EC.alert_is_present())  # Wait for alert to appear
            alert = driver.switch_to.alert  # Switch to the alert
            alert_text = alert.text  # Get the alert text
            assert alert_text == "Comment status updated successfully.", f"Unexpected alert text: {alert_text}"
            alert.accept()  # Close the alert

            # Verify if the comment state is changed to 'CLEAN' or appropriate
            WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element(
                    (By.CLASS_NAME, "comment-item-admin"),
                    "CLEAN"
                )
            )

            break  # Exit after handling the matched comment
