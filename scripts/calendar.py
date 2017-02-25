EMAIL = "your_email_here"


def calendar(args, calendar):
    if len(args) < 3:
        return ["Sorry, it seems like you are using the command improperly, be sure to remember the format is:\n`!calendar add ; <Title> ; <Date in format YYYY-MM-DD> ; <Start time in format HH:mm> ; <End time in format HH:mm> ; <Description> ; <Location>`"]  # noqa: 501
    elif args[1] == "add":
        return add(args, calendar)


def add(args, calendar):
    TITLE = DATE = STIME = ETIME = LOCATION = DESCRIPTION = ""
    l = [TITLE, DATE, STIME, ETIME, DESCRIPTION, LOCATION]
    i = -1
    for x in range(2, len(args)):
        if args[x] == ";":
            i += 1
        l[i] = l[i] + args[x] + " "

    TITLE = str(l[0])
    DATE = str(l[1])
    STIME = str(l[2])
    ETIME = str(l[3])
    DESCRIPTION = str(l[4])
    LOCATION = str(l[5])

    event = {}
    event['creator'] = {}
    event['creator']['self'] = False
    event['creator']['displayName'] = 'PantherBot'
    event['summary'] = TITLE[2:-1]
    event['description'] = DESCRIPTION[2:-1]
    event['location'] = LOCATION[2:-1]
    event['start'] = {}
    event['start']['dateTime'] = DATE[2:-1] + 'T' + STIME[2:-1] + ':00.000'
    event['start']['timeZone'] = 'America/New_York'
    event['end'] = {}
    event['end']['dateTime'] = DATE[2:-1] + 'T' + ETIME[2:-1] + ':00.000'
    event['end']['timeZone'] = 'America/New_York'

    print "submitting request"
    event = calendar.events().insert(calendarId='primary', body=event).execute()  # noqa: 401
    return ["Event successfully created: " + event.get('htmlLink')]
