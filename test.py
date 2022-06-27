import unittest
from time import sleep

from selenium import webdriver


class TestGetPage(unittest.TestCase):
    def test_get_page_proxy(self):
        # https://free-proxy-list.net/

        proxy = '45.149.43.56:53281'
        proxy_settings = {
            "proxyType": "MANUAL",
            "httpProxy": proxy,
            "sslProxy": proxy,
        }

        url = "http://porhovsky.psk.sudrf.ru"
        title = "Порховский районный суд Псковской области"

        # Set selenium configuration (run at docker container)
        options = webdriver.FirefoxOptions()

        options.set_capability('proxy', proxy_settings)

        selenium_grid_url = "http://0.0.0.0:4444/wd/hub"

        with webdriver.Remote(command_executor=selenium_grid_url,
                              options=options) as browser:
            browser.set_page_load_timeout(300)

            # browser.get('https://www.find-ip.net/')

            # Get page
            browser.get(url)
            test_title = browser.title

            # Stop browser
            sleep(5)
            browser.close()

        self.assertEqual(test_title, title, f"Title '{title}' not in page title. Actual is '{test_title}'.")

    def test_get_page(self):
        url = "http://porhovsky.psk.sudrf.ru"
        title = "Порховский районный суд Псковской области"

        # Set selenium configuration (run at docker container)
        options = webdriver.FirefoxOptions()

        selenium_grid_url = "http://0.0.0.0:4444/wd/hub"

        with webdriver.Remote(command_executor=selenium_grid_url,
                              options=options) as browser:
            browser.set_page_load_timeout(300)

            # Get page
            browser.get(url)
            test_title = browser.title

            # Stop browser
            sleep(5)
            browser.close()

        self.assertEqual(test_title, title, f"Title '{title}' not in page title. Actual is '{test_title}'.")

    def test_docker_selenium(self):
        selenium_grid_url = "http://0.0.0.0:4444/wd/hub"

        # https://selenium-python.readthedocs.io/api.html
        driver = webdriver.Remote(options=webdriver.FirefoxOptions(),
                                  command_executor=selenium_grid_url)

        driver.maximize_window()
        driver.minimize_window()
        driver.get("https://www.google.com/")
        title = driver.title

        # close the browser
        driver.close()

        self.assertEqual(title, "Google", f"Expected title is Google, get - '{title}'.")


if __name__ == "__main__":
    unittest.main()
