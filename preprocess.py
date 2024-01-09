import re
import pandas as pd
from dateutil import parser


def parse_dates_with_fallback(dates, primary_format, fallback_format):
    parsed_dates = pd.to_datetime(dates, format=primary_format, errors='coerce')
    fallback_dates = pd.to_datetime(dates[parsed_dates.isna()], format=fallback_format, errors='coerce')
    parsed_dates[parsed_dates.isna()] = fallback_dates
    return parsed_dates
def preprocess_data(data , mode):

    time_form = "12hr" if re.search(r'(?i)AM|PM', data.split(" - ", 1)[0]) else "24hr"

    if time_form == "12hr":
        pattern = '\d{1,4}[/.-]\d{1,4}[/.-]\d{1,4},\s\d{1,2}:\d{1,2}\s[aApP][mM]\s-\s'
    else:
        pattern = '\d{1,4}[/.-]\d{1,4}[/.-]\d{1,4},\s\d{1,2}:\d{1,2}\s-\s'

    msgs = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'msgs': msgs, 'dates': dates})

    # df['dates'] = df['dates'].apply(lambda x: parser.parse(x.replace(' ', ' ').replace(', ', ' ').replace(' - ', ' '), fuzzy=True , dayfirst=True))

    if time_form == "12hr":
        if mode == 'dmy':
            df['dates'] = parse_dates_with_fallback(df['dates'], '%d/%m/%Y, %I:%M %p - ', '%d/%m/%y, %I:%M %p - ')
            # df['dates'] = pd.to_datetime(df['dates'], format='%d/%m/%Y, %I:%M %p - ', errors='coerce')
        elif mode == 'mdy':
            df['dates'] = parse_dates_with_fallback(df['dates'], '%m/%d/%Y, %I:%M %p - ', '%m/%d/%y, %I:%M %p - ')
            # df['dates'] = pd.to_datetime(df['dates'], format='%d/%m/%Y, %I:%M %p - ', errors='coerce')
        elif mode == 'ymd':
            df['dates'] = parse_dates_with_fallback(df['dates'], '%Y/%m/%d, %I:%M %p - ', '%y/%m/%d, %I:%M %p - ')
            # df['dates'] = pd.to_datetime(df['dates'], format='%d/%m/%Y, %I:%M %p - ', errors='coerce')
        elif mode == 'ydm':
            df['dates'] = parse_dates_with_fallback(df['dates'], '%Y/%d/%m, %I:%M %p - ', '%y/%d/%m, %I:%M %p - ')
    else:
        if mode == 'dmy':
            df['dates'] = parse_dates_with_fallback(df['dates'], '%d/%m/%Y, %H:%M - ', '%d/%m/%y, %H:%M - ')
            # df['dates'] = pd.to_datetime(df['dates'], format='%d/%m/%Y, %H:%M - ', errors='coerce')
        elif mode == 'mdy':
            df['dates'] = parse_dates_with_fallback(df['dates'], '%m/%d/%Y, %H:%M - ', '%m/%d/%y, %H:%M - ')
            # df['dates'] = pd.to_datetime(df['dates'], format='%d/%m/%Y, %H:%M - ', errors='coerce')
        elif mode == 'ymd':
            df['dates'] = parse_dates_with_fallback(df['dates'], '%Y/%m/%d, %H:%M - ', '%y/%m/%d, %H:%M - ')
            # df['dates'] = pd.to_datetime(df['dates'], format='%d/%m/%Y, %H:%M - ', errors='coerce')
        elif mode == 'ydm':
            df['dates'] = parse_dates_with_fallback(df['dates'], '%Y/%d/%m, %H:%M - ', '%y/%d/%m, %H:%M - ')

    # elif mode == '2d':
    #     df['dates'] = pd.to_datetime(df['dates'], format='%d/%m/%Y, %H:%M - ', errors='coerce')
    # elif mode == '1m':
    #     df['dates'] = pd.to_datetime(df['dates'], format='%m/%d/%y, %I:%M %p - ', errors='coerce')
    # elif mode == '2m':
    #     df['dates'] = pd.to_datetime(df['dates'], format='%m/%d/%y, %H:%M - ', errors='coerce')

    df['date'] = df['dates']

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    users = []
    messages = []
    for msg in df['msgs']:
        parts = msg.split(':', 1)

        if parts[1:]:
            users.append(parts[0])
            messages.append(parts[1])
        else:
            users.append('System_message')
            messages.append(parts[0])

    df['username'] = users
    df['message'] = messages

    df['messages2'] = df['message'].apply(lambda x: x.replace("\n", " "))

    df = df.drop(['msgs', 'dates', 'date', 'only_date', 'message'], axis='columns')
    df['msg'] = df['messages2']
    df = df.drop('messages2', axis='columns')

    # days_dict = {'Monday': 'a', 'Tuesday': 'b', 'Wednesday': 'c', 'Thursday': 'd', 'Friday': 'e', 'Saturday': 'f',
    #              'Sunday': 'g'}
    # df['day_order'] = df['day_name']
    # df['day_order'] = df['day_order'].apply(lambda x: days_dict[x])
    df['period'] = (df['hour']).astype(str).str.zfill(2) + "-" + (df['hour'] + 1).astype(str).str.zfill(2)

    # df['period'] = df['hour'] + 1
    # df['period'] = df['period'].astype(str)
    #
    # for i in range(df['hour'].shape[0]):
    #     s1 = str(df['hour'][i])
    #     t1 = "0" + s1 if len(s1) == 1 else s1
    #     s2 = str(df['period'][i])
    #     t2 = "0" + s2 if len(s2) == 1 else s2
    #
    #     df['period'][i] = t1 + "-" + t2

    df["day_name"] = df["day_name"].astype(pd.api.types.CategoricalDtype(
        categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]))

    return df
