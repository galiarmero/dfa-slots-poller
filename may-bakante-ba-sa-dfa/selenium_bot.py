import os
import sys
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


class SeleniumBot(object):
    def __init__(self):
        self._session = requests.Session();
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
            page_source = self._driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            token = soup.find_all('input', attrs={'name': '__RequestVerificationToken'})

            cookies = self._get_driver_cookies()
            res = self._session.post('https://www.passport.gov.ph/countries', data={'regionId': 1})
            countries_json = res.json()
            ph_country_id_list = [ country['Id'] for country in countries_json['Countries'] \
                                                if country['Name'] == 'Philippines' ]
            ph_country_id = 0 if not ph_country_id_list else ph_country_id_list[0]
            
            
            res = self._session.post('https://www.passport.gov.ph/sites', \
                                        data={'regionId': 1, 'countryId': ph_country_id})
            sites_json = res.json()

            self._check_slot_availability(sites_json['Sites'])
        except ValueError as err:
            print(err.msg)
        except NoSuchWindowException:
            print("Hooman closed the browser.")
        except WebDriverException as err:
            print(err.msg)

    
    def _check_slot_availability(self, sites):
        site_option_xpath_pattern = "//select[@id='SiteID']/option[@value={}]"
        for site in sites:
            try:
                print("Checking site {} - {}".format(site['Id'], site['Name']))
                site_option_xpath = site_option_xpath_pattern.format(site['Id'])
                self._driver.find_element_by_xpath(site_option_xpath).click()
                self._driver.find_element_by_xpath("//button[@type='submit' and @value='next']").click()

            except NoSuchElementException as ex:
                print(ex.msg)


    def _get_driver_cookies(self):
        driver_cookies = self._driver.get_cookies()
        return { c['name']: c['value'] for c in driver_cookies }


if __name__ == "__main__":
    bot = SeleniumBot()
    bot.run()