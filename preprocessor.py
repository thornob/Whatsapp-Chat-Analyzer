import re
import pandas as pd

def parse_date(date_str):
    for fmt in ('%d/%m/%Y, %H:%M', '%d/%m/%y, %H:%M', '%d/%m/%Y, %I:%M %p', '%d/%m/%y, %I:%M %p'):
        try:
            return pd.to_datetime(date_str, format=fmt)
        except ValueError:
            continue
    return pd.NaT

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[APap][Mm])?\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    dates = [d.strip(" -") for d in dates]
    parsed_dates = [parse_date(d) for d in dates]

    df = pd.DataFrame({'user_message': messages, 'message_date': parsed_dates})
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([^:]+):\s', message, maxsplit=1)
        if len(entry) > 2:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Add time breakdown
    df['only_date'] =df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['day_name'] = df['date'].dt.day_name()
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour ==23:
            period.append(str('hour') + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df
