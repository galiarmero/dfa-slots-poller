import json

from constants import SITES_JSON
from db_factory import DBFactory

class SaveSites(object):
    def execute(self):
        try:
            sites = self._load_sites()
            db = DBFactory.create()
            db.sites.delete_many({})
            db.sites.insert_many(sites)

        except Exception as ex:
            print("{}: {}".format(type(ex).__name__, ex))


    def _load_sites(self):
        with open(SITES_JSON) as datafile:
            return json.load(datafile)


if __name__ == "__main__":
    save_sites = SaveSites()
    save_sites.execute()
