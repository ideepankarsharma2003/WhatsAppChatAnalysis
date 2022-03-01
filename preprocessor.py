import re
import pandas as pd

def preprocess(data):
    pattern= '\d{1,2}/\d{1,2}/\d{1,2}, \d{1,2}:\d{1,2} \s?(?:a|p)\.?m\.? - +'
    messages = re.split(pattern, data)[1:]


    dates = re.findall(pattern, data)
    df= pd.DataFrame({'user_messsage': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%y, %I:%M %p - ")
    df.rename(columns={'message_date': 'date'}, inplace=True)
    # df.head(10)
    lstU = []  # list for users
    lstM = []  # list for messages
    # msg = "Aanchal BCA changed this group's icon"
    for msg in df['user_messsage']:
        entry = re.split('([\w\W]+?):\s', msg)
        print(entry)

        if entry[1:]:
            lstU.append(entry[1])
            lstM.append(entry[2])
        else:
            lstU.append('group_notification')
            lstM.append(entry[0])

    # print(lstU)
    # print(lstM)
    df['user']= lstU
    df['message'] = lstM
    df.drop(columns=['user_messsage'], inplace=True)
    # df.head()
    df['year'] = df['date'].dt.year  # get years from date
    # df.head()
    df['month'] = df['date'].dt.month_name()  # get the name of months
    # df.head()

    df['day'] = df['date'].dt.day  # get the day
    df['hour'] = df['date'].dt.hour  # get the hour
    df['minute'] = df['date'].dt.minute  # get the minute


    df['day_name'] = df['date'].dt.day_name()

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str("00"))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour+1))
        else:
            period.append(str(hour) + '-' + str(hour+1))


    df['period'] = period



    # df.head(20)
    return df
