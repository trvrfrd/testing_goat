from .base import FunctionalTest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        # we go to the dang web site to get our to-do lists
        self.browser.get(self.live_server_url)

        # we see that the web site is about To-Do things
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # we should be able to enter a new to-do item first thing
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # we type "wash my face" into a text box
        inputbox.send_keys("wash my face")

        # when we hit enter, the page upates, and now the page lists
        # "1: wash your face" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: wash my face")

        # these is still a text box for adding another item
        # enter "brush my teeth" (it's hard to even do the basics these days)
        inputbox = self.get_item_input_box()
        inputbox.send_keys("brush my teeth")
        inputbox.send_keys(Keys.ENTER)

        # the page updates and shows both items in the list
        self.wait_for_row_in_list_table("1: wash my face")
        self.wait_for_row_in_list_table("2: brush my teeth")


    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys("wash my face")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: wash my face")

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # Now a new user comes along

        ## clear browser session, cookies, etc.
        ## to simulate separate users
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page
        # There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("wash my face", page_text)
        self.assertNotIn("brush my teeth", page_text)

        # Francis starts a new list by entering an item
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("wash my face", page_text)
        self.assertIn("Buy milk", page_text)

        # everyone is happy forever
