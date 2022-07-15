import pytest

from page_objects_and_tests_for_opencart.pages.admin_login_page import AdminLoginPage
from page_objects_and_tests_for_opencart.pages.admin_dashboard_page import AdminDashboardPage
from page_objects_and_tests_for_opencart.pages.add_product_page import AddNewProductPage
from page_objects_and_tests_for_opencart.pages.admin_products_page import AdminProductsPage


@pytest.fixture(scope="function")
def login_as_admin(browser, base_url, user):
    admin_login_page = AdminLoginPage(browser, base_url)
    admin_login_page.open()
    admin_login_page.fill_field_login_page(user["username"], user["password"])
    login_button = admin_login_page.wait_element(AdminLoginPage.LOCATORS["login button"])
    login_button.click()
    return AdminDashboardPage(browser, base_url)


@pytest.fixture(scope="function")
def go_to_products(browser, base_url, login_as_admin, logged_in=False):
    if logged_in:
        page = AdminDashboardPage(browser, base_url)
        page.wait_element(page.LOCATORS["open catalog"]).click()
        page.wait_element(page.LOCATORS["catalog: products"]).click()
        return AdminProductsPage(browser, base_url)
    # go to Products from Dashboard after login
    login_as_admin.go_to_products()
    return AdminProductsPage(browser, base_url)


@pytest.fixture(scope="function")
def go_to_add_new_product_page(browser, base_url, go_to_products):
    # click "Add New" on the Products page
    go_to_products.click_add_new_product()
    return AddNewProductPage(browser, base_url)
