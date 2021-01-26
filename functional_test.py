from selenium import webdriver
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
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # we should be able to enter a new to-do item first thing

        # we type "wash my face" into a text box

        # when we hit enter, the page upates, and now the page lists
        # "1: wash your face" as an item in a to-do list

        # these is still a text box for adding another item. enter
        # "brush your teeth" (it's hard to even do the basics these days)

        # the page updates and shows both items in the list

        # see that the site has generated a unique URL for saving our list
        # and there is some explanatory text to that effect

        # we visit the URL and see that our to-do list is still there

        # great we did it

if __name__ == "__main__":
    unittest.main()
