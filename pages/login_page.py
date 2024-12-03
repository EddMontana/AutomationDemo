from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from pages.page import Page


class LoginPage(Page):
    def __init__(self, driver):
        super().__init__(driver)
        """
        Initialize the Login Page.
        """
        self.username_text_field = (AppiumBy.ACCESSIBILITY_ID, "test-Username")
        self.password_text_field = (AppiumBy.ACCESSIBILITY_ID, "test-Password")
        self.login_button = (AppiumBy.ACCESSIBILITY_ID, "test-LOGIN")

    def perform_login(self, username, password) -> None:
        """ 
        Perform login with the given username and password.
        """
        self.driver.find_element(*self.username_text_field).clear()
        self.driver.find_element(*self.username_text_field).send_keys(username)
        self.driver.find_element(*self.password_text_field).clear()
        self.driver.find_element(*self.password_text_field).send_keys(password)
        self.driver.find_element(*self.login_button).click()

    def is_error_message_present(self, text) -> bool:
        """
        Check if the error message is present.
        """
        try:
            return self.driver.find_element(AppiumBy.XPATH, f'//android.widget.TextView[@text="{text}"]').is_displayed()
        except NoSuchElementException:
            return False
