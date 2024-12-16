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

def test_rate_movie_success(login_user, db_session):
    driver = login_user
    # Navigate to the movie page
    driver.get("http://localhost:8080/movie/2")  # Change this URL to the movie page URL
    time.sleep(3)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "rating-5")))  # Wait for the rating option
    rating_element = driver.find_element(By.ID, "rating-5")   
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@for='rating-5']"))
    ).click()
    time.sleep(3)
    # Check if the rating was saved correctly by checking the star selection
    assert driver.find_element(By.ID, "rating-5").is_selected(), "Rating was not saved correctly."

    user = user_crud.get_user_by_email(db_session, "user2@example.com")
    movies = movie_crud.get_user_rated_movies(db_session, user.id)
    movie = movie_crud.get_movie(db_session, 2)
    assert any(m['title'] == movie.title for m in movies), f"Movie '{movie.title}' is not in the rated movies list."

    movie_crud.remove_rate_movie(db_session, user.id, 2)

def test_rating_logged_out_user(driver_setup, db_session):
    driver = driver_setup
    # Navigate to the movie page without logging in
    driver.get("http://localhost:8080/movie/3")
    time.sleep(3)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "rating-5")))  # Wait for the rating option
    rating_element = driver.find_element(By.ID, "rating-5")   
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@for='rating-5']"))
    ).click()

    '''# Handle the alert and check the text
    WebDriverWait(driver, 20).until(EC.alert_is_present())  # Wait for alert to appear
    alert = driver.switch_to.alert  # Switch to the alert
    alert_text = alert.text  # Get the alert text
    assert alert_text == "You must log in to rate a movie.", f"Unexpected alert text: {alert_text}"
    alert.accept()  # Close the alert
    '''
    # Verify the user was redirected to the login page
    WebDriverWait(driver, 20).until(EC.url_contains("login"))

    # Verify that the user was redirected to the login page
    assert "login" in driver.current_url, "User was not redirected to login page."

def test_remove_rating_success(login_user, db_session):
    driver = login_user
    driver.get("http://localhost:8080/movie/4")

    # Select a rating (5 stars)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "rating-5")))  # Wait for the rating option
    rating_element = driver.find_element(By.ID, "rating-5")   
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@for='rating-5']"))
    ).click()

    time.sleep(3)

    user = user_crud.get_user_by_email(db_session, "user2@example.com")
    movies = movie_crud.get_user_rated_movies(db_session, user.id)
    movie = movie_crud.get_movie(db_session, 4)
    assert any(m['title'] == movie.title for m in movies), f"Movie '{movie.title}' is not in the rated movies list."

    # Now click the same rating again to remove it
    rating_element = driver.find_element(By.ID, "rating-5")   
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@for='rating-5']"))
    ).click()
    time.sleep(3)
    # Ensure the rating is removed (the radio button should no longer be selected)
    assert not driver.find_element(By.ID, "rating-5").is_selected(), "Rating was not removed successfully."

    user = user_crud.get_user_by_email(db_session, "user2@example.com")
    movies = movie_crud.get_user_rated_movies(db_session, user.id)
    movie = movie_crud.get_movie(db_session, 4)
    assert all(m['title'] != movie.title for m in movies), f"Movie '{movie.title}' is unexpectedly in the rated movies list."



def test_rating_functionality_on_movie_page(login_user, db_session):
    driver = login_user
    driver.get("http://localhost:8080/movie/5")

    # Rate with 1, 3, and 5 stars in sequence to check proper functionality
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "rating-1")))  # Wait for the rating option
    rating_element = driver.find_element(By.ID, "rating-1")   
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@for='rating-1']"))
    ).click()
    time.sleep(3)
    assert driver.find_element(By.ID, "rating-1").is_selected(), "Rating 1 was not saved correctly."

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "rating-3")))  # Wait for the rating option
    rating_element = driver.find_element(By.ID, "rating-3")   
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@for='rating-3']"))
    ).click()
    time.sleep(3)
    assert driver.find_element(By.ID, "rating-3").is_selected(), "Rating 3 was not saved correctly."

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "rating-5")))  # Wait for the rating option
    rating_element = driver.find_element(By.ID, "rating-5")   
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@for='rating-5']"))
    ).click()
    time.sleep(3)
    assert driver.find_element(By.ID, "rating-5").is_selected(), "Rating 5 was not saved correctly."

    
    user = user_crud.get_user_by_email(db_session, "user2@example.com")
    movies = movie_crud.get_user_rated_movies(db_session, user.id)
    movie = movie_crud.get_movie(db_session, 5)
    assert any(m['title'] == movie.title for m in movies), f"Movie '{movie.title}' is not in the rated movies list."

    movie_crud.remove_rate_movie(db_session, user.id, 5)

def test_check_list_actualization(login_user, db_session):
    driver = login_user
    driver.get("http://localhost:8080/movie/6")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "rating-2")))  # Wait for the rating option
    rating_element = driver.find_element(By.ID, "rating-2")   
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@for='rating-2']"))
    ).click()
    time.sleep(2)
    assert driver.find_element(By.ID, "rating-2").is_selected(), "Rating 2 was not saved correctly."

    user = user_crud.get_user_by_email(db_session, "user2@example.com")
    movies = movie_crud.get_user_rated_movies(db_session, user.id)
    movie = movie_crud.get_movie(db_session, 6)
    assert any(m['title'] == movie.title for m in movies), f"Movie '{movie.title}' is not in the rated movies list."
    
    driver.get("http://localhost:8080/profile")
    time.sleep(2)

    # Verify that the user was redirected to the profile page
    assert "profile" in driver.current_url, "User was not redirected to profile page."
    
    # Wait for the profile page to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "profile-page"))
    )

    # Click on the "Rated Movies" button if not active
    rated_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Rated Movies')]")
    if "active" not in rated_button.get_attribute("class"):
        rated_button.click()

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
    # Check if the movie with id=1 is in the rated list
    movie_item = driver.find_element(By.XPATH, "//div[@class='movie-item']//a[contains(@href, '/movie/6')]")
    ActionChains(driver).move_to_element(movie_item).perform()
    assert movie_item.is_displayed(), "Movie with id=6 is not displayed in the Rated Movies list."
    
    
    time.sleep(3) 

    movie_crud.remove_rate_movie(db_session, user.id, 6)