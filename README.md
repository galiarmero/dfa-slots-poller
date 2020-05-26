# May Bakante Ba Sa DFA?

Easily check for available timeslots from DFA's [Passport Appointment System](https://www.passport.gov.ph/).


# Config

If data is intended to be saved to a database (MongoDB), `DB_HOST`, `DB_PORT`, and `DB_NAME` environment variables should be set.

Make sure packages in `may-bakante-ba-sa-dfa/requirements.txt` are installed.


# Usage

## Poll available timeslots
1. Print to console the available timeslots for all DFA sites
    ```
    python may-bakante-ba-sa-dfa/poll_available_timeslots.py
    ```

2. Save to database the available timeslots for all DFA sites. Availability for a site is only saved if numbers changed from previous poll
    ```
    python may-bakante-ba-sa-dfa/poll_available_timeslots.py --save-db
    ```

## Update static list of DFA sites and poll available timeslots

```bash
python may-bakante-ba-sa-dfa/main.py  # print to console
python may-bakante-ba-sa-dfa/main.py --save-db # save to DB
```


