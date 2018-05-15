import os
import sys
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


class SeleniumBot(object):
    def __init__(self):
        self._session = requests.Session()
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

            res = self._session.post('https://www.passport.gov.ph/countries', data={'regionId': 1})
            countries_json = res.json()
            ph_country_id = self._get_ph_country_id(countries_json['Countries'])
            
            res = self._session.post('https://www.passport.gov.ph/sites', \
                    data={'regionId': 1, 'countryId': ph_country_id})
            sites_json = res.json()


            res = self._session.post('https://www.passport.gov.ph/appointment/individual/site', \
                    data={'__RequestVerificationToken': self._get_request_verif_token_field(), \
                            'HasForeignPassport': False,  'OffsetTicks': 0, 'SiteRegionID': 1, \
                            'SiteCountryID': 1, 'SiteID': 24, 'NextStep': 'schedule', \
                            'CurrentStep': 'site', 'submitcommand': 'next'})


            schedule_xhr_headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'Origin': 'https://www.passport.gov.ph',
                'Referer': 'https://www.passport.gov.ph/appointment/individual/schedule'
            }

            
            res = self._session.post('https://www.passport.gov.ph/appointment/timeslot/available/next', \
                    data={'requestDate': '2018-05-16', 'maxDate': '2018-09-30', 'siteId': 24, 'slots': 1}, \
                    headers=schedule_xhr_headers)
            next_available_timeslot_json = res.json();

            res = self._session.post('https://www.passport.gov.ph/appointment/timeslot/available', \
                    data={'fromDate': '2018-05-16', 'toDate': '2019-01-20', 'siteId': 24, 'requestedSlots': 1}, \
                    headers=schedule_xhr_headers)
            timeslots_availbility = res.json()


        except ValueError as ex:
            print("{}: {}".format(type(ex).__name__, ex))
        except NoSuchWindowException as ex:
            print("Hooman closed the browser.")
            print("{}: {}".format(type(ex).__name__, ex))
        except WebDriverException as ex:
            print("{}: {}".format(type(ex).__name__, ex))

    
    def _get_ph_country_id(self, countries):
        ph_country_id_list = [ country['Id'] for country in countries \
                                            if country['Name'] == 'Philippines' ]
        return 0 if not ph_country_id_list else ph_country_id_list[0]


    def _get_request_verif_token_field(self):
        page_source = self._driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        return soup.find('input', attrs={'name': '__RequestVerificationToken'})['value']


    def _get_driver_cookies(self):
        driver_cookies = self._driver.get_cookies()
        return { c['name']: c['value'] for c in driver_cookies }


if __name__ == "__main__":
    bot = SeleniumBot()
    bot.run()