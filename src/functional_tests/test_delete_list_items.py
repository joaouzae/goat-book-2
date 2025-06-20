from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest
from functional_tests.list_page import ListPage


class TestDeleteItems(FunctionalTest):
    def setUp(self):
        super().setUp()
        self.create_pre_authenticated_session("edith@example.com")

    def test_delete_item_from_list(self):
        # Edith is a logged-in user who visits Superlists homepage
        # She starts a list
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item("To be deleted")

        # Edith notices there's an "x" button on the item
        trs: list[WebElement] = list_page.get_table_rows()
        print(trs[0].find_element(By.CLASS_NAME, "btn-close"))

        # She clicks it
        trs[0].find_element(By.CLASS_NAME, "btn-close").click()

        # Now she notices the item is gone from the list and the list is empty
        trs: list[WebElement] = list_page.get_table_rows()
        self.assertEqual(trs, [])

        # She refreshes the page and the item is still gone
        self.browser.get(self.browser.current_url)
        trs: list[WebElement] = list_page.get_table_rows()
        self.assertEqual(trs, [])

        # Edith goes back to My Lists page and see the list (whose title was
        # the name of its first item, which is gone) is gone
        self.browser.find_element(By.LINK_TEXT, "My lists").click()
        self.wait_for(lambda: self.browser.find_element(By.TAG_NAME, "ul"))
        ul = self.browser.find_element(By.TAG_NAME, "ul")

        self.assertEqual(ul.find_elements(By.CSS_SELECTOR, "*"), [])
