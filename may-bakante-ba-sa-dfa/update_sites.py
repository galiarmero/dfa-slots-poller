import os
import json
import cfscrape
import argparse
from constants import SITES_JSON
from db_factory import DBFactory


APAC_REGION_ID = 1 # Asia Pacific

COUNTRIES_URI = 'https://www.passport.gov.ph/countries'
SITES_URI = 'https://www.passport.gov.ph/sites'

class UpdateSites(object):
    def __init__(self):
        self._scraper = cfscrape.create_scraper()


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
        res = self._scraper.post(COUNTRIES_URI, data={'regionId': APAC_REGION_ID}, verify=False)
        print("country")
        print(res.text)
        countries = res.json()['Countries']
        ph_country_id_list = [ country['Id'] for country in countries \
                                            if country['Name'] == 'Philippines' ]
        return 0 if not ph_country_id_list else ph_country_id_list[0]


    def _get_sites(self, country_id):
        res = self._scraper.post(SITES_URI, \
                data={'regionId': APAC_REGION_ID, 'countryId': country_id}, verify=False)
        print("sites")
        print(res.text)
        return self._format_sites(res.json()['Sites'])


    def _format_sites(self, sites):
        return [ { self._format_key(k): self._format_value(k, v) \
                    for k, v in site.items() } for site in sites ]


    def _format_key(self, k):
        return "siteId" if k == 'Id' else k.lower()


    def _format_value(self, k, v):
        if k == 'Address':
            return v.replace('\r\n', ' ').strip()
        if k == 'Telephone':
            return v.replace('\t', ' ').strip()
        return v


if __name__ == "__main__":
    parser = argparse.ArgumentParser( \
        description="Get all DFA sites through the DFA Passport Appointment website")
    args = parser.parse_args()

    update_sites = UpdateSites()
    update_sites.execute()
