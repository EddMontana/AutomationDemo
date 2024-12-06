import pytest
import logging

from pages.main_page import MainPage
from pages.login_page import LoginPage

logger = logging.getLogger("login")


#test all incorrect login scenarios
@pytest.mark.parametrize("username, password, expected_error_message",
    [
        ("", "incorrect_password","Username is required"),    # username is empty
        ("","","Username is required"),    # both username and password are empty
        ("standard_user","","Password is required"),    # password is empty
        ("standard_user","incorrect_password","Username and password do not match any user in this service."), # incorrect password
        ("incorrect_user","incorrect_password","Username and password do not match any user in this service."),  # incorrect user
        ("locked_out_user","secret_sauce","Sorry, this user has been locked out."),  # locked out user    
    ]
)
def test_incorrect_login(driver, username, password, expected_error_message):
    """
    Objective: Verify that the error message is displayed when incorrect login credentials are provided.
    Steps:
        1. Enter incorrect login credentials.
        2. Verify that the error message is correctly displayed.
    """
    login_page = LoginPage(driver)
    logger.info(f"Attempt to log in with username: '{username}' and password: '{password}'")
    
    # Ensure login page is visible 
    assert login_page.get_element(login_page.login_button).is_displayed(), "Login page has not loaded: Login button si not displayed"
    
    login_page.perform_login(username, password)
    
    # ensure error message is displayed correctly
    assert login_page.is_error_message_present(expected_error_message), f"Expected error message '{expected_error_message}' not present"

# Test correct login credentials
def test_correct_login(driver):
    """
    Objective: Verify that the user can log in with correct credentials.
    Steps:
        1. Enter correct login credentials.
        2. Verify that the user is successfully logged in.
    """
    login_page = LoginPage(driver)

    # Ensure login page is visible 
    assert login_page.get_element(login_page.login_button).is_displayed(), "Login page has not loaded: Login button si not displayed"

    # Perform correct login
    login_page.perform_login("standard_user", "secret_sauce")

    # Ensure home page is loaded: successfully logged in
    main_page = MainPage(driver)
    assert main_page.get_element(main_page.inventory_title).is_displayed(), "Main page not loaded: Inventory screen is not displayed after login!"




