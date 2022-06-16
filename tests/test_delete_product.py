from pages.admin_products_page import AdminProductsPage


def test_add_new_product_and_delete(browser, base_url, go_to_add_new_product_page):
    """Create product filling only required fields: name, meta, model"""
    add_new_product_page = go_to_add_new_product_page
    created_product = add_new_product_page.create_product()
    products_page = AdminProductsPage(browser, base_url)
    products_page.filter_and_select_the_exact_product(created_product["name"])
    products_page.delete_selected_products()
    assert products_page.filter_products_by(name=created_product["name"]).get_products_number_on_page() == 0, \
        f"Didn't expect to find the product '{created_product['name']}' on page after deletion, but found it!"


def test_should_be_alert_on_delete_action(browser, base_url, go_to_add_new_product_page):
    """Create product filling only required fields: name, meta, model"""
    add_new_product_page = go_to_add_new_product_page
    created_product = add_new_product_page.create_product()
    products_page = AdminProductsPage(browser, base_url)
    products_page.filter_and_select_the_exact_product(created_product["name"])
    products_page.click(products_page.LOCATORS["delete"])
    assert products_page.wait_alert(), \
        f"Expected to get an alert after pressing the delete button, but didn't find one."
    products_page.wait_alert().accept()


def test_should_not_delete_product_if_dismiss_alert(browser, base_url, go_to_add_new_product_page):
    add_new_product_page = go_to_add_new_product_page
    created_product = add_new_product_page.create_product()
    products_page = AdminProductsPage(browser, base_url)
    products_page.filter_and_select_the_exact_product(created_product["name"])
    products_page.click(products_page.LOCATORS["delete"])
    assert products_page.wait_alert(), \
        f"Expected to get an alert after pressing the delete button, but didn't find one."
    products_page.wait_alert().dismiss()
    assert products_page.filter_products_by(name=created_product["name"]).get_products_number_on_page() == 1, \
        f"Expect to find the product '{created_product['name']}' on page, because it should not been deleted, " \
        f"but didn't found it!"
