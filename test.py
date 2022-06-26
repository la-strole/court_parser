import unittest
from selenium import webdriver
from time import sleep


class TestGetPage(unittest.TestCase):
    def test_get_page(self):
        url = "http://pechorsky.psk.sudrf.ru"
        title = "Печорский районный суд Псковской области"

        # Set selenium configuration (run at docker container)
        options = webdriver.FirefoxOptions()
        selenium_grid_url = "http://0.0.0.0:4444/wd/hub"
        browser = webdriver.Remote(command_executor=selenium_grid_url,
                                   options=options)
        # Get page
        browser.get(url)
        test_title = browser.title

        # Stop browser
        sleep(5)
        browser.quit()

        self.assertEqual(test_title, title, f"Title {title} not in page title. Actual is {test_title}")


if __name__ == "__main__":
    unittest.main()
