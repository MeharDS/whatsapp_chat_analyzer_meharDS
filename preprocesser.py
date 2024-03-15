import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s\w{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    #Make DataFrame
    df= pd.DataFrame({'user_massage':messages, 'massage_date':dates})

    # convert message_date type
    df['massage_date'] = df['massage_date'].str.replace("-","").str.strip()
    df['massage_date'] = df['massage_date'].str.replace("/",".")
    df['massage_date'] = df['massage_date'].str.replace(",","")
    df['massage_date'] = pd.to_datetime(df['massage_date'])

    df.rename(columns={'massage_date':'date'}, inplace=True)

    users=[]
    massages=[]
    for massage in df['user_massage']:
        entry = re.split('([\w\W]+?):\s', massage)
        if entry[1:]: #user_name
            users.append(entry[1])
            massages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            massages.append(entry[0])
    
    df['users'] = users
    df['massages'] = massages
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_name']=df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day'] = df['date'].dt.day_name()
    df['hour']= df['date'].dt.hour
    df['minute']= df['date'].dt.minute
    df['second']= df['date'].dt.second

    period = []
    for hour in df[['day', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

def preprocess_24(data):
        pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

        messages = re.split(pattern, data)[1:]
        dates = re.findall(pattern, data)

        df = pd.DataFrame({'user_message': messages, 'message_date': dates})
        # convert message_date type
        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')

        df.rename(columns={'message_date': 'date'}, inplace=True)

        users = []
        messages = []
        for message in df['user_message']:
                entry = re.split('([\w\W]+?):\s', message)
                if entry[1:]:  # user name
                        users.append(entry[1])
                        messages.append(" ".join(entry[2:]))
                else:
                        users.append('group_notification')
                        messages.append(entry[0])

        df['users'] = users
        df['massages'] = messages
        df.drop(columns=['user_message'], inplace=True)

        df['only_date'] = df['date'].dt.date
        df['year'] = df['date'].dt.year
        df['month_num'] = df['date'].dt.month
        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['day_name'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute

        period = []
        for hour in df[['day_name', 'hour']]['hour']:
                if hour == 23:
                        period.append(str(hour) + "-" + str('00'))
                elif hour == 0:
                        period.append(str('00') + "-" + str(hour + 1))
                else:
                        period.append(str(hour) + "-" + str(hour + 1))

        df['period'] = period

        return df
