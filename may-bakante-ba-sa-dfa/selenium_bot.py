import os
import sys
import requests

class SeleniumBot(object):
    def __init__(self):
        self._session = requests.Session()


    def run(self):
        try:
            res = self._session.post('https://www.passport.gov.ph/countries', data={'regionId': 1})
            countries_json = res.json()
            ph_country_id = self._get_ph_country_id(countries_json['Countries'])
            
            res = self._session.post('https://www.passport.gov.ph/sites', \
                    data={'regionId': 1, 'countryId': ph_country_id})
            sites_json = res.json()

            schedule_xhr_headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'Origin': 'https://www.passport.gov.ph',
                'Referer': 'https://www.passport.gov.ph/appointment/individual/schedule'
            }

            
            res = self._session.post('https://www.passport.gov.ph/appointment/timeslot/available/next', \
                    data={'requestDate': '2018-05-16', 'maxDate': '2019-05-16', 'siteId': 24, 'slots': 1}, \
                    headers=schedule_xhr_headers)
            next_available_timeslot_json = res.json()
            print(next_available_timeslot_json)

            res = self._session.post('https://www.passport.gov.ph/appointment/timeslot/available', \
                    data={'fromDate': '2018-05-16', 'toDate': '2019-05-16', 'siteId': 24, 'requestedSlots': 1}, \
                    headers=schedule_xhr_headers)
            timeslots_availbility = res.json()
            print(timeslots_availbility)


        except Exception as ex:
            print("{}: {}".format(type(ex).__name__, ex))

    
    def _get_ph_country_id(self, countries):
        ph_country_id_list = [ country['Id'] for country in countries \
                                            if country['Name'] == 'Philippines' ]
        return 0 if not ph_country_id_list else ph_country_id_list[0]


if __name__ == "__main__":
    bot = SeleniumBot()
    bot.run()