CASE 1: No cookies yet

GOTO /appointment/individual/site

    /appointment/individual/site            GET     200 OK
    /appointment/individual/site            POST    200 OK
    /countries                              POST    200 OK
    /sites                                  POST    200 OK


CHOOSE SITE
CLICK NEXT

    /appointment/individual/site            POST    302 Found
    /appointment/individual/schedule        GET     200 OK
    /appointment/timeslot/available/next    POST    200 OK
    /appointment/timeslot/available         POST    200 OK