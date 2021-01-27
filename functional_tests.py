from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorText(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # we do to the dang web site to get our to-do lists
        self.browser.get("http://localhost:8000")

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
        time.sleep(1)

        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertTrue(
            any(row.text == "1: wash my face" for row in rows)
        )

        # these is still a text box for adding another item. enter
        # "brush your teeth" (it's hard to even do the basics these days)
        self.fail("Finish the test!")

        # the page updates and shows both items in the list

        # see that the site has generated a unique URL for saving our list
        # and there is some explanatory text to that effect

        # we visit the URL and see that our to-do list is still there

        # great we did it

if __name__ == "__main__":
    unittest.main()