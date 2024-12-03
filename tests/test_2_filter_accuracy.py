import logging
import pytest

from pages.main_page import MainPage
from pages.login_page import LoginPage

logger = logging.getLogger("filter_accuracy")
login_credentials = ("standard_user", "secret_sauce")

#parameterized test for filter
@pytest.mark.parametrize("filter_type, filter_value",
    [
        ("name", "ascending"),
        ("name", "descending"),
        ("price", "ascending"),
        ("price", "descending")
    ]
    )
def test_filter(driver, filter_type, filter_value):
    """
    Objective: Verify that the name filter works as expected.
    Steps:
        1. Perform login.
        2. Set the filter according to the test parameters.
        3.Verify that the products are sorted in the correct order.
    """
    logger.info(f"Sorting products in {filter_value} order by name.")
    login_page = LoginPage(driver)
    # Perform valid login
    login_page.perform_login(*login_credentials)

    home_page = MainPage(driver)
    home_page.toggle_grid_view()
    
    # set the filter
    home_page.set_filter(filter_type, filter_value)
    
    #create list  of products
    products_list = []
    #create set of products to flter out duplicates
    products_set = set()

    # add products to the list and set until no new products are loaded
    loaded_new_products = True
    while loaded_new_products:
        loaded_new_products = False
        new_products = home_page.get_available_items()

        for product in new_products:
            if product not in products_set:
                products_list.append(product)
                products_set.add(product)
                loaded_new_products = True

        # scroll down to load more products
        home_page.scroll_down()


    #check if the products are sorted in the correct order based on the filter type and filter value
    check_list = []
    
    if filter_type == "name":
        if filter_value == "ascending":
            check_list = sorted(products_list, key=lambda x: x[0])
        elif filter_value == "descending":
            check_list = sorted(products_list, key=lambda x: x[0], reverse=True)
    elif filter_type == "price":
        if filter_value == "ascending":
            check_list = sorted(products_list, key=lambda x: float(x[1].replace("$", "")))
        elif filter_value == "descending":
            check_list = sorted(products_list, key=lambda x: float(x[1].replace("$", "")), reverse=True)


    assert check_list == products_list, f"Products are not sorted in {filter_value} order by {filter_type}."

