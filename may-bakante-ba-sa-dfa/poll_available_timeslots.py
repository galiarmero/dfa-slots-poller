import json
import requests
import datetime
import time
import argparse
from constants import SITES_JSON


AVAILABLE_TIMESLOT_URI = 'https://www.passport.gov.ph/appointment/timeslot/available'

SCHEDULE_XHR_HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://www.passport.gov.ph',
    'Referer': 'https://www.passport.gov.ph/appointment/individual/schedule'
}

class PollAvailableTimeslots(object):
    def __init__(self):
        self._session = requests.Session()


    def execute(self, print_mode):
        try:
            sites = self._load_sites()
            current_date, year_after_date = self._get_from_to_dates()
            process_data = self._print_data if print_mode else self._aggregate_data
            collection_time = int(round(time.time() * 1000))
            self._timeslot_availability = []

            for site in sites:
                available_timeslots = self._get_timeslots_availability(current_date, year_after_date, site['Id'])
                process_data(site['Name'], available_timeslots, collection_time)

            if not print_mode:
                # TODO: Save in database
                print(self._timeslot_availability)

        except Exception as ex:
            print("{}: {}".format(type(ex).__name__, ex))


    def _aggregate_data(self, site_name, available_timeslots, collection_time):
        self._timeslot_availability.append({
            'siteName': site_name,
            'availableTimeslots': available_timeslots,
            'collectionTime': collection_time
        })


    def _print_data(self, site_name, available_timeslots, collection_time):
        print()
        print(site_name)
        print(' > Available ({})'.format(len(available_timeslots)))

        if len(available_timeslots):
            print('    {}'.format('\n    '.join([ self._millis_to_date(a) for a in available_timeslots])))


    def _load_sites(self):
        with open(SITES_JSON) as datafile:
            return json.load(datafile)


    def _get_timeslots_availability(self, from_date, to_date, site_id):
        timeslots = self._session.post(AVAILABLE_TIMESLOT_URI, \
                data={'fromDate': from_date, 'toDate': to_date, 'siteId': site_id, 'requestedSlots': 1}, \
                headers=SCHEDULE_XHR_HEADERS).json()

        return [ t['AppointmentDate'] for t in timeslots if t['IsAvailable'] ]


    def _get_from_to_dates(self):
        today = datetime.date.today()
        return today.strftime('%Y-%m-%d'), \
                (today + datetime.timedelta(days=365)).strftime('%Y-%m-%d')


    def _millis_to_date(self, millis):
        try:
            return datetime.datetime.fromtimestamp(millis / 1000.0) \
                                    .strftime('%a, %b %d %Y %I:%M %p')
        except TypeError:
            return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser( \
        description="Poll available timeslots from DFA's Passport Appointment System")
    parser.add_argument('-p', '--print-mode', action='store_true', \
        help="Print available timeslots in console instead of saving in database")
    args = parser.parse_args()

    poll_timeslots = PollAvailableTimeslots()
    poll_timeslots.execute(args.print_mode)
