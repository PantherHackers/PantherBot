import datetime
import pandas
from collections import Counter
from sqlalchemy import create_engine
engine = create_engine('mysql://root@localhost:3306/pantherbot_test', echo=False)

def g_r(response, args):
    if args[0] == 'time':
        if len(args)!=4:
            return ["ERROR: Please use the following syntax `time <channel> 2/1/17 5/1/18`"]
        return time(args[2::], args[1])

    if args[0] == 'top_users':
        pass

    if args[0] == 'emoji':
        pass

    if args[0] == 'channel':
        pass

    if args[0] == 'help':
        return """
        List of arguments for GenerateReport (g_r)

        time (g_r time random 12/01/15 5/01/17)
            -- Returns time related data on the channel specified, if none given
            then default is slack-wide.
            -- Takes 3 arguments: <channel> <begin date> <end date>
        """


def time(range, channel='all'):
    try:
        v = [datetime.datetime.strptime(x, "%m/%d/%y").date() for x in range]
    except ValueError:
        return ["Please input time in the syntax of mm/dd/yy"]
    q = None
    if channel == 'all':
        q = engine.execute("SELECT hour FROM channelActivity WHERE day_of_month >= %s and day_of_month <= %s and month >= %s and month <= %s and year >= %s and year <= %s", v[0].day, v[1].day, v[0].month, v[1].month, v[0].year, v[1].year).fetchall()
    else:
        q = engine.execute("SELECT hour FROM channelActivity WHERE channel_id = (SELECT slack_id FROM channels WHERE name = %s) and day_of_month >= %s and day_of_month <= %s and month >= %s and month <= %s and year >= %s and year <= %s", channel, v[0].day, v[1].day, v[0].month, v[1].month, v[0].year, v[1].year).fetchall()

    cnt = Counter()
    for v in q:
        cnt[v[0]] += 1


    i = 1
    hour=[]
    count=[]
    while i <= 24:
        hour.append(i)
        count.append(cnt[i])
        i += 1

    print hour
    df = pandas.DataFrame({'Count':count}, index=hour)
    df.columns.name = 'Hour'
    return [str(df)]
 