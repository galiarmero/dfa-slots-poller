import os
import sys
import requests
from selenium import webdriver


class SeleniumBot(object):
    def __init__(self):
        executable_path = os.path.abspath(
            os.path.join(os.getcwd(), 'chromedriver.exe'))
        try:
            self._driver = webdriver.Chrome(executable_path)
        except WebDriverException as err:
            print("{0}".format(err))
            sys.exit()


    def run(self):
        try:
            self._driver.get('https://www.passport.gov.ph/appointment/individual/site')
        except NoSuchWindowException:
            print("Hooman closed the browser.")
        except WebDriverException as err:
            print(err.msg)


if __name__ == "__main__":
    bot = SeleniumBot()
    bot.run()