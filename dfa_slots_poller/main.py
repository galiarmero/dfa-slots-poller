import argparse

from poll_available_timeslots import PollAvailableTimeslots
from update_sites import UpdateSites

if __name__ == "__main__":
    parser = argparse.ArgumentParser( \
        description="A Python client for checking available timeslots in " \
                    "DFA's Passport Appointment System")
    parser.add_argument('-u', '--update-sites', action='store_true', \
        help="Update the stored list of DFA sites before checking available timeslots")
    parser.add_argument('-p', '--print-mode', action='store_true', \
        help="Print available timeslots in console instead of saving in database")
    args = parser.parse_args()

    if args.update_sites:
        update_sites = UpdateSites()
        update_sites.execute()

    poll_slots = PollAvailableTimeslots()
    poll_slots.execute(args.print_mode)