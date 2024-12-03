from selenium.common.exceptions import NoSuchElementException
from typing import Optional, Tuple, List


class Page:
    def __init__(self, driver, default_wait_time=10): # default wait time is 10 seconds
        """
        Initialize the Page.
        """
        self.driver = driver
        self.driver.implicitly_wait(default_wait_time)


    def get_element(self, element) -> None:
        """
        Get the element if present.
        """
        try:
            return self.driver.find_element(*element)   # * is used to unpack the tuple
        except NoSuchElementException:
            return None

    def set_wait(self, wait_time) -> None:
        """
        Set the wait time.
        """
        self.driver.implicitly_wait(wait_time)
    
