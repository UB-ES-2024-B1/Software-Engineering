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

def test_like_movie_success(login_user, db_session):
    driver = login_user
    # Navigate to the movie page
    driver.get("http://localhost:8080/movie/2")  
    time.sleep(3)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "like-toggle")))  # Wait for the liking option
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='checkmark']"))
    )
    
    # Locate the div with the checkmark using XPath
    checkmark_div = driver.find_element(By.XPATH, "//div[@class='checkmark']")
    
    
    # Click the checkbox to toggle like
    checkmark_div.click()
    time.sleep(3)
    
    # Assert the checkbox is selected after clicking
    assert driver.find_element(By.ID, "like-toggle").is_selected(), "Liking was not saved correctly."

    user = user_crud.get_user_by_email(db_session, "user2@example.com")
    movies = movie_crud.get_user_liked_movies(db_session, user.id)
    movie = movie_crud.get_movie(db_session, 2)
    assert any(m == movie.title for m in movies), f"Movie '{movie.title}' is not in the liked movies list."

    movie_crud.remove_movie_like(db_session, 2, user.id)

def test_non_like_movie_success(login_user, db_session):
    driver = login_user
    # Navigate to the movie page
    driver.get("http://localhost:8080/movie/3")  
    time.sleep(3)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "like-toggle")))  # Wait for the liking option
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='checkmark']"))
    )
    
    # Locate the div with the checkmark using XPath
    checkmark_div = driver.find_element(By.XPATH, "//div[@class='checkmark']")
    
    
    # Click the checkbox to toggle like
    checkmark_div.click()
    time.sleep(3)
    
    # Assert the checkbox is selected after clicking
    assert driver.find_element(By.ID, "like-toggle").is_selected(), "Liking was not saved correctly."
    
    # Click the checkbox to toggle like
    checkmark_div.click()
    time.sleep(3)
    
    # Assert the checkbox is not selected after clicking
    assert not driver.find_element(By.ID, "like-toggle").is_selected(), "Liking was not saved correctly."

    user = user_crud.get_user_by_email(db_session, "user2@example.com")
    movies = movie_crud.get_user_liked_movies(db_session, user.id)
    movie = movie_crud.get_movie(db_session, 3)
    assert all(m != movie.title for m in movies), f"Movie '{movie.title}' is unexpectedly in the liked movies list."

def test_liking_logged_out_user(driver_setup, db_session):
    driver = driver_setup
    # Navigate to the movie page without logging in
    driver.get("http://localhost:8080/movie/3")
    time.sleep(3)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "like-toggle")))  # Wait for the liking option
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='checkmark']"))
    )
    
    # Locate the div with the checkmark using XPath
    checkmark_div = driver.find_element(By.XPATH, "//div[@class='checkmark']")
    
    # Click the checkbox to toggle like
    checkmark_div.click()

    '''# Handle the alert and check the text
    WebDriverWait(driver, 20).until(EC.alert_is_present())  # Wait for alert to appear
    alert = driver.switch_to.alert  # Switch to the alert
    alert_text = alert.text  # Get the alert text
    assert alert_text == "You must log in to give like a movie.", f"Unexpected alert text: {alert_text}"
    alert.accept()  # Close the alert
    '''
    # Verify the user was redirected to the login page
    WebDriverWait(driver, 20).until(EC.url_contains("login"))

    # Verify that the user was redirected to the login page
    assert "login" in driver.current_url, "User was not redirected to login page."

def test_check_list_actualization(login_user, db_session):
    driver = login_user
    driver.get("http://localhost:8080/movie/6")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "like-toggle")))  # Wait for the liking option
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='checkmark']"))
    )
    
    # Locate the div with the checkmark using XPath
    checkmark_div = driver.find_element(By.XPATH, "//div[@class='checkmark']")
    
    # Click the checkbox to toggle like
    checkmark_div.click()

    time.sleep(2)
    assert driver.find_element(By.ID, "like-toggle").is_selected(), "Liking was not saved correctly."

    user = user_crud.get_user_by_email(db_session, "user2@example.com")
    movies = movie_crud.get_user_liked_movies(db_session, user.id)
    movie = movie_crud.get_movie(db_session, 6)
    assert any(m == movie.title for m in movies), f"Movie '{movie.title}' is not in the liked movies list."

    driver.get("http://localhost:8080/profile")
    time.sleep(2)

    # Verify that the user was redirected to the profile page
    assert "profile" in driver.current_url, "User was not redirected to profile page."
    
    # Wait for the profile page to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "profile-page"))
    )

    # Click on the "Favourite Movies" button if not active
    liked_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Favourite Movies')]")
    if "active" not in liked_button.get_attribute("class"):
        liked_button.click()

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
    # Check if the movie with id=1 is in the liked list
    movie_item = driver.find_element(By.XPATH, "//div[@class='movie-item']//a[contains(@href, '/movie/6')]")
    ActionChains(driver).move_to_element(movie_item).perform()
    assert movie_item.is_displayed(), "Movie with id=6 is not displayed in the Favourite Movies list."
    
    time.sleep(3) 

    movie_crud.remove_movie_like(db_session, 6, user.id)