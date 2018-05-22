import os
import json
import requests
from constants import SITES_JSON


APAC_REGION_ID = 1 # Asia Pacific

COUNTRIES_URI = 'https://www.passport.gov.ph/countries'
SITES_URI = 'https://www.passport.gov.ph/sites'

class UpdateSites(object):
    def __init__(self):
        self._session = requests.Session()


    def execute(self):
        try:
            ph_country_id = self._get_ph_country_id()
            sites = self._get_sites(ph_country_id)

            self._update_sites_json(sites)

        except Exception as ex:
            print("{}: {}".format(type(ex).__name__, ex))


    def _update_sites_json(self, sites):
        with open(SITES_JSON, 'w') as outfile:
            json.dump(sites, outfile, indent=4)


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


if __name__ == "__main__":
    update_sites = UpdateSites()
    update_sites.execute()