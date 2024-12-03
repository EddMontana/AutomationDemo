from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from pages.page import Page
import logging
from typing import Optional, Tuple, List


logger = logging.getLogger("main_page")

class MainPage(Page):
    def __init__(self, driver):
        super().__init__(driver)
        """
        Initialize the Main Page.
        """
        self.inventory_title = (AppiumBy.XPATH, '//android.widget.TextView[@text="PRODUCTS"]')

    
    	
    def toggle_grid_view(self) -> None:
        """
        Toggle the grid view of the items.
        """
        grid_view_button = self.driver.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[@content-desc="test-Toggle"]/android.widget.ImageView')
        grid_view_button.click()
            
    def get_available_items(self) -> Optional[List[Tuple[str, str]]]:
        try:
            items = self.driver.find_elements(By.XPATH, '//android.view.ViewGroup[@content-desc="test-Item"]')
            # log the number of items found
            logger.info(f"Number of items found: {len(items)}")
            products = []
            for item in items:
                # log the title of each item found
                try:
                    items_title = item.find_element(By.XPATH, './/android.widget.TextView[@content-desc="test-Item title"]').get_attribute('text') #.// to signify that the search is within the item and searches in all the children not just direct children
                except NoSuchElementException:
                    continue
                try:
                    items_price = item.find_element(By.XPATH, './/android.widget.TextView[@content-desc="test-Price"]').get_attribute('text')
                except NoSuchElementException:
                    continue
                logger.info(f"Item title: {items_title}, Item price: {items_price}")
                products.append((items_title, items_price))
            return products
        except NoSuchElementException:
            return None

    def set_filter(self,filter_type, filter_value) -> None:
        """
        Set the filter for the items.
        """
        filter_button = self.driver.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-Modal Selector Button"]')
        filter_button.click()

        if filter_type == "name":
            if filter_value == "ascending":
                filter_option = self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Name (A to Z)"]')
                filter_option.click()
            elif filter_value == "descending":
                filter_option = self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Name (Z to A)"]')
                filter_option.click()
        elif filter_type == "price":
            if filter_value == "ascending":
                filter_option = self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Price (low to high)"]')
                filter_option.click()
            elif filter_value == "descending":
                filter_option = self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Price (high to low)"]')
                filter_option.click()
	
    def scroll_down(self) -> None:
        """
        Scroll down to load more items.
        """
        self.driver.swipe(500, 1500, 500, 300, 1000)  # swipe from (500, 1500) to (500, 300) in 1 second 