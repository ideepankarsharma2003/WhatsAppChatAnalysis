from collections import Counter
import emoji
import pandas as pd
from urlextract import URLExtract
extractor = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user!='Overall':
        df= df[df['user']== selected_user]


    #  1. number of messages
    num_messages= df.shape[0]

    #  2. number of words
    words= []
    for message in df['message']:
        # print(message)
        words.extend(message.split())

    #  3. number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    #  4. number of links shared
    links=[]
    for message in df['message']:
        # print(extractor.find_urls(message))
        links.extend((extractor.find_urls(message)))
    
    return num_messages, len(words), num_media_messages, len((links))


    # else:
    #     new_df = df[df['user'] == selected_user]
    #     #  1. number of messages
    #     num_messages = new_df.shape[0]
    #     #  2. number of words
    #     words = []
    #     for message in new_df['message']:
    #         # print(message)
    #         words.extend(message.split())
    #     return num_messages, len(words)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index': 'names', 'user': 'percentage'})

    return x, df
    


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Removing Group Notifications and Media Messages !!!
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\r\n']
    temp = temp[temp['message'] != '<Media omitted>\n']
    # temp = temp[temp['message'] != '<media omitted>']

    # removing stop words
    f = open('hinglish.txt', 'r')
    stop_words = f.read()
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df= pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['message']:
        emojis.extend(
            # [c for c in message if c in emoji.UNICODE_EMOJI_ALIAS_ENGLISH])
            [c for c in message if c in emoji.UNICODE_EMOJI['en']])
    emoji_df= pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df= emoji_df.rename(columns={0: "Emoji", 1:"Usage"})
    return emoji_df



def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]


    df['month_num'] = df['date'].dt.month    
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    
    time = []


    for i in range(timeline.shape[0]):
        # print(timeline['month'][i]+ '-'+ str(timeline['year'][i]))
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time']= time
    
    return timeline

    


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['day_num'] = df['date'].dt.date    
    daily_timeline = df.groupby('day_num').count()['message'].reset_index()    
    
    return daily_timeline




def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
   
    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
   
    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    pivot_table= pd.pivot_table(df, index='day_name', columns='period', values='message', aggfunc='count')
    
   
    return pivot_table.fillna(0)



