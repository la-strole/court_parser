from selenium import webdriver

import time

selenium_grid_url = "http://0.0.0.0:4444/wd/hub"
print("Test Execution Started")
time.sleep(10)
driver = webdriver.Remote(options=webdriver.FirefoxOptions(),
                          command_executor=selenium_grid_url)

print('maximize the window size')
driver.maximize_window()
time.sleep(10)
driver.minimize_window()
print('navigate to browserstack.com')
driver.get("https://www.google.com/")
time.sleep(10)
print(driver.title)
time.sleep(10)
# close the browser
driver.close()
print("Test Execution Successfully Completed!")
