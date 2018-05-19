import os
import sys
import requests


APAC_REGION_ID = 1 # Asia Pacific

COUNTRIES_URI = 'https://www.passport.gov.ph/countries'
SITES_URI = 'https://www.passport.gov.ph/sites'
NEXT_AVAILABLE_TIMESLOT_URI = 'https://www.passport.gov.ph/appointment/timeslot/available/next'
AVAILABLE_TIMESLOT_URI = 'https://www.passport.gov.ph/appointment/timeslot/available'

SCHEDULE_XHR_HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://www.passport.gov.ph',
    'Referer': 'https://www.passport.gov.ph/appointment/individual/schedule'
}

class SeleniumBot(object):
    def __init__(self):
        self._session = requests.Session()


    def run(self):
        try:
            ph_country_id = self._get_ph_country_id()
            sites = self._get_sites(ph_country_id)
            next_available_timeslot = self._get_next_available_timeslot( \
                '2018-05-16', '2019-05-16', 24)
            timeslots_availability = self._get_timeslots_availability( \
                '2018-05-16', '2019-05-16', 24)
            
            print(next_available_timeslot, timeslots_availability)

        except Exception as ex:
            print("{}: {}".format(type(ex).__name__, ex))

    
    def _get_ph_country_id(self):
        res = self._session.post(COUNTRIES_URI, data={'regionId': APAC_REGION_ID})
        countries = res.json()['Countries']
        ph_country_id_list = [ country['Id'] for country in countries \
                                            if country['Name'] == 'Philippines' ]
        return 0 if not ph_country_id_list else ph_country_id_list[0]


    def _get_sites(self, country_id):
        res = self._session.post(SITES_URI, \
                data={'regionId': APAC_REGION_ID, 'countryId': country_id})
        return res.json()['Sites']


    def _get_next_available_timeslot(self, from_date, to_date, site_id):
        return self._session.post(NEXT_AVAILABLE_TIMESLOT_URI, \
                data={'requestDate': from_date, 'maxDate': to_date, 'siteId': site_id, 'slots': 1}, \
                headers=SCHEDULE_XHR_HEADERS).json()


    def _get_timeslots_availability(self, from_date, to_date, site_id):
        return self._session.post(AVAILABLE_TIMESLOT_URI, \
                data={'fromDate': from_date, 'toDate': to_date, 'siteId': site_id, 'requestedSlots': 1}, \
                headers=SCHEDULE_XHR_HEADERS).json()


if __name__ == "__main__":
    bot = SeleniumBot()
    bot.run()