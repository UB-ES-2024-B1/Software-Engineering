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
'''
def test_wish_movie_success(login_user, db_session):
    driver = login_user
    # Navigate to the movie page
    driver.get("http://localhost:8080/movie/2")  # Change this URL to the movie page URL
    time.sleep(3)

    # Wait for the element to be clickable
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@class='ui-bookmark wishlist-button']/div[@class='bookmark']"))
    )

    # Locate the element
    bookmark_div = driver.find_element(By.XPATH, "//label[@class='ui-bookmark wishlist-button']/div[@class='bookmark']")

    time.sleep(1)  # Optional: Let the page settle after scrolling

    # Now click the element
    bookmark_div.click()
    time.sleep(3)

    # Check if the checkbox inside the label is selected 
    checkbox = driver.find_element(By.XPATH, "//label[@class='ui-bookmark wishlist-button']/input[@type='checkbox']")
    assert checkbox.is_selected(), "The wishlist state is not selected after the click."
    
    user = user_crud.get_user_by_email(db_session, "user2@example.com")
    movies = movie_crud.get_user_wished_movies(db_session, user.id)
    movie = movie_crud.get_movie(db_session, 2)
    assert any(m == movie.title for m in movies), f"Movie '{movie.title}' is not in the wish movies list."

    movie_crud.remove_wish_movie(db_session, user.id, 2)

def test_non_wish_movie_success(login_user, db_session):
    driver = login_user
    # Navigate to the movie page
    driver.get("http://localhost:8080/movie/3")  # Change this URL to the movie page URL
    time.sleep(3)

    # Wait for the element to be clickable
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@class='ui-bookmark wishlist-button']/div[@class='bookmark']"))
    )

    # Locate the element
    bookmark_div = driver.find_element(By.XPATH, "//label[@class='ui-bookmark wishlist-button']/div[@class='bookmark']")

    time.sleep(1)  # Optional: Let the page settle after scrolling

    # Now click the element
    bookmark_div.click()
    time.sleep(3)

    # Check if the checkbox inside the label is selected 
    checkbox = driver.find_element(By.XPATH, "//label[@class='ui-bookmark wishlist-button']/input[@type='checkbox']")
    assert checkbox.is_selected(), "The wishlist state is not selected after the click."
    
    # Now click the element
    bookmark_div.click()
    time.sleep(3)

    # Check if the checkbox inside the label is selected
    checkbox = driver.find_element(By.XPATH, "//label[@class='ui-bookmark wishlist-button']/input[@type='checkbox']")
    assert not checkbox.is_selected(), "The wishlist state is not selected after the click."

    user = user_crud.get_user_by_email(db_session, "user2@example.com")
    movies = movie_crud.get_user_wished_movies(db_session, user.id)
    movie = movie_crud.get_movie(db_session, 3)
    assert all(m != movie.title for m in movies), f"Movie '{movie.title}' is unexpectedly in the wish movies list."

def test_wishing_logged_out_user(driver_setup, db_session):
    driver = driver_setup
    # Navigate to the movie page without logging in
    driver.get("http://localhost:8080/movie/3")

    
    # Wait for the element to be clickable
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@class='ui-bookmark wishlist-button']/div[@class='bookmark']"))
    )

    # Locate the element
    bookmark_div = driver.find_element(By.XPATH, "//label[@class='ui-bookmark wishlist-button']/div[@class='bookmark']")

    time.sleep(1)  # Optional: Let the page settle after scrolling

    # Now click the element
    bookmark_div.click()
    time.sleep(3)
   
    # Handle the alert and check the text
    WebDriverWait(driver, 20).until(EC.alert_is_present())  # Wait for alert to appear
    alert = driver.switch_to.alert  # Switch to the alert
    alert_text = alert.text  # Get the alert text
    assert alert_text == "You must log in to add to your wishlist.", f"Unexpected alert text: {alert_text}"
    alert.accept()  # Close the alert

    # Verify the user was redirected to the login page
    WebDriverWait(driver, 20).until(EC.url_contains("login"))

    # Verify that the user was redirected to the login page
    assert "login" in driver.current_url, "User was not redirected to login page."


def test_check_list_actualization(login_user, db_session):
    driver = login_user
    driver.get("http://localhost:8080/movie/6")

    
    # Wait for the element to be clickable
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@class='ui-bookmark wishlist-button']/div[@class='bookmark']"))
    )

    # Locate the element
    bookmark_div = driver.find_element(By.XPATH, "//label[@class='ui-bookmark wishlist-button']/div[@class='bookmark']")

    time.sleep(1)  # Optional: Let the page settle after scrolling

    # Now click the element
    bookmark_div.click()
    time.sleep(3)

    # Check if the checkbox inside the label is selected 
    checkbox = driver.find_element(By.XPATH, "//label[@class='ui-bookmark wishlist-button']/input[@type='checkbox']")
    assert checkbox.is_selected(), "The wishlist state is not selected after the click."
    

    user = user_crud.get_user_by_email(db_session, "user2@example.com")
    movies = movie_crud.get_user_wished_movies(db_session, user.id)
    movie = movie_crud.get_movie(db_session, 6)
    assert any(m == movie.title for m in movies), f"Movie '{movie.title}' is not in the wished movies list."

    driver.get("http://localhost:8080/profile")
    time.sleep(2)

    # Verify that the user was redirected to the profile page
    assert "profile" in driver.current_url, "User was not redirected to profile page."
    
    # Wait for the profile page to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "profile-page"))
    )

    # Click on the "Wishlist Movies" button if not active
    wish_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Wishlist Movies')]")
    if "active" not in wish_button.get_attribute("class"):
        wish_button.click()

    # Wait for the movies list to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "movies-list"))
    )

    # Scroll the movie list into view to ensure all items are accessible
    movies_list = driver.find_element(By.CLASS_NAME, "movies-list")
    driver.execute_script("arguments[0].scrollIntoView(true);", movies_list)

    # Wait for the movie items to render (if lazy-loaded or dynamically updated)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='movie-item']"))
    )

    time.sleep(3) 
    # Check if the movie with id=1 is in the wished list
    movie_item = driver.find_element(By.XPATH, "//div[@class='movie-item']//a[contains(@href, '/movie/6')]")
    ActionChains(driver).move_to_element(movie_item).perform()
    assert movie_item.is_displayed(), "Movie with id=6 is not displayed in the Wishlist Movies list."
    
    time.sleep(3) 

    movie_crud.remove_wish_movie(db_session, user.id, 6)'''