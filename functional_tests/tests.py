from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time


MAX_WAIT = 5


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()


    def tearDown(self):
        self.browser.quit()


    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()

        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.1)


    def test_can_start_a_list_and_retrieve_it_later(self):
        # we do to the dang web site to get our to-do lists
        self.browser.get(self.live_server_url)

        # we see that the web site is about To-Do things
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # we should be able to enter a new to-do item first thing
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # we type "wash my face" into a text box
        inputbox.send_keys("wash my face")

        # when we hit enter, the page upates, and now the page lists
        # "1: wash your face" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: wash my face")

        # these is still a text box for adding another item
        # enter "brush my teeth" (it's hard to even do the basics these days)
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("brush my teeth")
        inputbox.send_keys(Keys.ENTER)

        # the page updates and shows both items in the list
        self.wait_for_row_in_list_table("1: wash my face")
        self.wait_for_row_in_list_table("2: brush my teeth")

        # see that the site has generated a unique URL for saving our list
        # and there is some explanatory text to that effect
        self.fail("Finish the test!")

        # we visit the URL and see that our to-do list is still there

        # great we did it
