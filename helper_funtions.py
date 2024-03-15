from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd 
from collections import Counter
import emoji

f = open('stop_hinglish.txt', 'r')
stop_words = f.read()


def fatch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    #fetch the number of messages
    num_messages = len(df['massages'])

    #fetch the total number of words
    words = []
    for massage in df['massages']:
        words.extend(massage.split())

    #fetch the total number of Media Shared
    num_media_messages = df[df['massages'] == '<Media omitted>\n']

    #fetch the total number of Links
    extract = URLExtract()
    num_links = []
    for massage in df['massages']:
        num_links.extend(extract.find_urls(massage))


    return num_messages, len(words), len(num_media_messages), len(num_links)


def most_busy_users(df):
    x = df['users'].value_counts().head()
    Busy_users_df = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index' : 'User_name', 'users' : 'Percent'})
    
    return x, Busy_users_df.head()

def create_wordcloud(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    new_df = remove_group_noti_medi_omit(df)
    new_df['massages'] = new_df['massages'].apply(remove_stop_words)
    
    wc = WordCloud(min_font_size=10,background_color='white')
    df_wc = wc.generate(new_df['massages'].str.cat(sep=" "))
    return df_wc

def remove_group_noti_medi_omit(df):
    new_df = df[df['users'] != 'group_notification']
    new_df = new_df[new_df['massages'] != '<Media omitted>\n']
    return new_df

def remove_stop_words(massage):

    y = []
    for word in massage.lower().split():
        if word not in stop_words:
            y.append(word)

    return " ".join(y)


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    new_df = remove_group_noti_medi_omit(df)
    
    words = []
    for massage in new_df['massages']:
        for word in massage.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_words = pd.DataFrame(Counter(words).most_common(10))

    return most_common_words


def emoji_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for massage in df['massages']:
        emojis.extend([c for c in massage if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(5))

    return emoji_df

def montly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    montly_timeline = df.groupby(['year', 'month_num', 'month_name']).count()['massages'].reset_index() #reset_index() convert it to DataFrame
    time = []
    for i in range (montly_timeline.shape[0]):
        time.append(montly_timeline['month_name'][i] + " " + str(montly_timeline['year'][i]))
    montly_timeline ['time']  = time
    return montly_timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline=df.groupby(['only_date']).count()['massages'].reset_index()
    return daily_timeline

def busy_day(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return  df['day'].value_counts()



def busy_month(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    return df['month_name'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    activity_map = df.pivot_table(index='day', columns='period', values='massages', aggfunc='count').fillna(0)
    return activity_map




























