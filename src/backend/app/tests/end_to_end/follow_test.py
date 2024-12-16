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

def test_follow_user_success(login_user, db_session):
    driver = login_user
    # Navigate to the movie page
    driver.get("http://localhost:8080/searchUsers") 
    time.sleep(3)


    # Capture the initial "Following" count from the sidebar
    following_count_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='stat'][3]/span[@class='stat-value']"))
    )
    initial_following_count = int(following_count_element.text)

    # Find a "Follow" button in the feed and click it
    follow_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'not-following') and contains(text(), 'Follow')]")
        )
    )
    follow_button.click()
    time.sleep(3)

    # Verify the button changes to "Following"
    assert "following" in follow_button.get_attribute("class").lower(), "The button did not update to 'Following'."

    user = user_crud.get_user_by_email(db_session, "user2@example.com")
    result = user_crud.get_followed_users(db_session, user.id)

    assert len(result)  == initial_following_count + 1, "Following count did not increase in backend."

    # Check that the "Following" count in the sidebar increases
    updated_following_count_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='stat'][3]/span[@class='stat-value']"))
    )
    updated_following_count = int(updated_following_count_element.text)
    assert updated_following_count == initial_following_count + 1, "Following count did not increase."

    # Find the "Following" button and click it to unfollow
    unfollow_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'following') and contains(text(), 'Following')]")
        )
    )
    unfollow_button.click()
    time.sleep(3)

    # Verify the button changes back to "Follow"
    assert "not-following" in unfollow_button.get_attribute("class").lower(), "The button did not update to 'Follow'."

    # Check that the "Following" count in the sidebar decreases
    final_following_count_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='stat'][3]/span[@class='stat-value']"))
    )
    final_following_count = int(final_following_count_element.text)
    assert final_following_count == initial_following_count, "Following count did not decrease."

    result = user_crud.get_followed_users(db_session, user.id)
    
    assert len(result)  == initial_following_count, "Following count did not decrease in backend."


def test_navigate_to_profile(login_user, db_session):
    driver = login_user

    # Navigate to the search users page
    driver.get("http://localhost:8080/searchUsers")
    time.sleep(3)

    # Locate a username link (router-link)
    username_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "username")
        )
    )

    # Capture the username text to verify after navigation
    username_text = username_link.text

    # Click the username link
    username_link.click()
    time.sleep(3)

    # Verify navigation to the user's profile page
    expected_url = f"http://localhost:8080/otherProfiles/{username_text}"
    WebDriverWait(driver, 10).until(EC.url_contains(expected_url))

    assert expected_url in driver.current_url, f"Did not navigate to the correct profile page. Current URL: {driver.current_url}"
    
    time.sleep(3)

    # Locate the followers count element
    followers_count_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'info-item') and contains(., 'Followers')]/h3")
        )
    )
    initial_followers_count = int(followers_count_element.text)

        
    # Locate the follow/unfollow button
    follow_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='follow-button']/button"))
    )
    initial_button_text = follow_button.text

    # Click the follow button
    follow_button.click()
    time.sleep(2)  # Allow time for the action to complete
    
    user = user_crud.get_user_by_email(db_session, "user2@example.com")
    final_following = user_crud.get_followed_users(db_session, user.id)


    # Verify that the button text changes appropriately
    updated_button_text = follow_button.text
    if initial_button_text == "Follow":
        assert updated_button_text == "Following", "Button text did not change to 'Following'"
    else:
        assert updated_button_text == "Follow", "Button text did not change to 'Follow'"

    # Check the followers count again
    updated_followers_count = int(followers_count_element.text)
    if initial_button_text == "Follow":
        assert updated_followers_count == initial_followers_count + 1, "Followers count did not increase"        
    else:
        assert updated_followers_count == initial_followers_count - 1, "Followers count did not decrease"        

    
    if initial_button_text == "Follow":
        assert any(follower.full_name == username_text for follower in final_following), f"{username_text} should be in the final_following list"
    else:
        assert not any(follower.full_name == username_text for follower in final_following), f"{username_text} should NOT be in the final_following list"
    
    initial_followers_count = int(followers_count_element.text)

    initial_button_text = follow_button.text
    # Click the follow button
    follow_button.click()
    time.sleep(2)  # Allow time for the action to complete
    
    
    final_following = user_crud.get_followed_users(db_session, user.id)


    # Verify that the button text changes appropriately
    updated_button_text = follow_button.text
    if initial_button_text == "Follow":
        assert updated_button_text == "Following", "Button text did not change to 'Following'"
    else:
        assert updated_button_text == "Follow", "Button text did not change to 'Follow'"

    # Check the followers count again
    updated_followers_count = int(followers_count_element.text)
    if initial_button_text == "Follow":
        assert updated_followers_count == initial_followers_count + 1, "Followers count did not increase"        
    else:
        assert updated_followers_count == initial_followers_count - 1, "Followers count did not decrease"        

    final_following = user_crud.get_followed_users(db_session, user.id)
    if initial_button_text == "Follow":
        assert any(follower.full_name == username_text for follower in final_following), f"{username_text} should be in the final_following list"
    else:
        assert not any(follower.full_name == username_text for follower in final_following), f"{username_text} should NOT be in the final_following list"
    