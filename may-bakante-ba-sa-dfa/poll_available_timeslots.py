import json
import requests
import datetime
from constants import SITES_JSON


NEXT_AVAILABLE_TIMESLOT_URI = 'https://www.passport.gov.ph/appointment/timeslot/available/next'
AVAILABLE_TIMESLOT_URI = 'https://www.passport.gov.ph/appointment/timeslot/available'

SCHEDULE_XHR_HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://www.passport.gov.ph',
    'Referer': 'https://www.passport.gov.ph/appointment/individual/schedule'
}

class PollAvailableTimeslots(object):
    def __init__(self):
        self._session = requests.Session()


    def execute(self):
        try:
            sites = self._load_sites()
            
            for site in sites:
                site_id = site['Id']
                next_available_timeslot = self._get_next_available_timeslot( \
                    '2018-05-16', '2019-05-16', site_id)
                available_timeslots = self._get_timeslots_availability( \
                    '2018-05-16', '2019-05-16', site_id)

                print(site['Name'])
                print(' > Next Available  : {}'.format(next_available_timeslot))
                print(' > Available {0:5s} : {1}'.format( \
                    '({})'.format(len(available_timeslots)), available_timeslots))

        except Exception as ex:
            print("{}: {}".format(type(ex).__name__, ex))


    def _load_sites(self):
        with open(SITES_JSON) as datafile:
            return json.load(datafile)


    def _get_next_available_timeslot(self, from_date, to_date, site_id):
        next_available = self._session.post(NEXT_AVAILABLE_TIMESLOT_URI, \
                data={'requestDate': from_date, 'maxDate': to_date, 'siteId': site_id, 'slots': 1}, \
                headers=SCHEDULE_XHR_HEADERS).json()

        return self._millis_to_date(next_available['Date']) if 'Date' in next_available else None


    def _get_timeslots_availability(self, from_date, to_date, site_id):
        timeslots = self._session.post(AVAILABLE_TIMESLOT_URI, \
                data={'fromDate': from_date, 'toDate': to_date, 'siteId': site_id, 'requestedSlots': 1}, \
                headers=SCHEDULE_XHR_HEADERS).json()

        return [ self._millis_to_date(t['AppointmentDate']) for t in timeslots if t['IsAvailable'] ]


    def _millis_to_date(self, millis):
        return datetime.datetime.fromtimestamp(millis / 1000.0) \
                                .strftime('%a, %b %d %Y %I:%M %p')
