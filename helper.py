import pandas as pd
import re
import matplotlib.pyplot as plt
from collections import Counter
import emoji
import seaborn as sns
import streamlit as st

plt.style.use('dark_background')



def get_stats(user , df):

    if user != "Overall":
        df = df[df['username'] == user]

    total_messages = df.shape[0]

    media_sent = df.loc[df['msg'].str.contains('<Media omitted>')].shape[0]

    total_emojis = 0
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]')
    for msg in df['msg']:
        total_emojis += len(emoji_pattern.findall(msg))

    total_words = 0
    for msg in df['msg']:
        total_words += len(msg.split())

    return total_messages, media_sent, total_words , total_emojis


def words_in_message(user,df):
    if user != "Overall":
        df = df[df['username'] == user]

    lengths = []
    for msg in df['msg']:
        lengths.append(len(msg.split()))

    counter = Counter(lengths).most_common()
    x = pd.DataFrame.from_records(list(dict(counter).items()), columns=['Words per Message', 'Message Count'])
    fig, ax = plt.subplots()
    ax.bar(x['Words per Message'][:30], x['Message Count'][:30], color='r')
    ax.set_xlim(0,50)
    ax.set_xlabel('Words per Message')
    ax.set_ylabel('Message Count')

    return fig , x.sort_values('Words per Message' , ascending=False).reset_index(drop=True)


def most_deleted_messages(df):
    tmp1 = df.loc[df['msg'].str.contains('You deleted this message')].value_counts(['username']).reset_index()
    tmp2 = df.loc[df['msg'].str.contains('This message was deleted')].value_counts(['username']).reset_index()
    del_df = pd.concat([tmp1, tmp2], ignore_index=True).sort_values('count' , ascending = False).reset_index(drop = True)
    del_df['%Percentage'] = round(100 * del_df['count'] / del_df['count'].sum(), 2)
    del_df = del_df.rename(columns={del_df.columns[0]: 'Username', 'count': 'Message Count'})

    fig, ax = plt.subplots()
    ax.barh(del_df['Username'][:15], del_df['Message Count'][:15], color='r')
    ax.set_title('Top Users (Most Deleted Messages)')
    ax.set_xlabel('Number of Deleted Messages')

    return fig , del_df



def msgs_by_user(df):
    countmsgs = df['username'].value_counts()
    fig, ax = plt.subplots()
    ax.barh(countmsgs.index[:15], countmsgs.values[:15], color='r')
    ax.set_title('Top Users (Most Messages Sent)')
    ax.set_xlabel('Number of Messages')

    um = pd.DataFrame(countmsgs).reset_index()
    um['%Percentage'] = round(100 * um['count'] / um['count'].sum(), 2)
    um = um.rename(columns={um.columns[0]: 'Username', 'count': 'Messages'})

    return fig, um



def most_common_words(agree , user ,df):

    if user != "Overall":
        df = df[df['username'] == user]


    if agree==0:
        f = open('stop_hinglish.txt', 'r')
        stoplist = f.read()
    else:
        stoplist = ['<media', 'omitted>']

    wordlist = []

    for msg in df['msg']:
        if 'This message was deleted' in msg or 'You deleted this message' in msg:
            continue
        for word in msg.split():
            if word in emoji.EMOJI_DATA:
                continue
            if word.lower() not in stoplist:
                wordlist.append(word.lower())

    counter = Counter(wordlist).most_common(500)
    list1 = [x[0] for x in counter]
    list2 = [x[1] for x in counter]
    fig, ax = plt.subplots()
    ax.set_title('Most Common Words' if agree==1 else 'Most Common Words (Without StopWords)')
    ax.barh(list1[:15], list2[:15], color='r')
    ax.set_xlabel('Word Occurence')

    return fig



def most_common_emojis(user , df):

    if user != "Overall":
        df = df[df['username'] == user]

    emojis = []
    for msg in df['msg']:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])

    if not emojis:
        return pd.DataFrame()

    counter = pd.DataFrame(Counter(emojis).most_common())
    counter = counter.rename(columns={counter.columns[0]:'Emoji' ,counter.columns[1]:'Count' })
    counter['%Percentage'] = round(100 * counter['Count'] / counter['Count'].sum(), 2)

    # list1 = [x[0] for x in counter]
    # list2 = [x[1] for x in counter]
    # fig, ax = plt.subplots()
    # ax.set_title('Most Common Emojis')
    # ax.barh(list1[:15], list2[:15], color='r')

    return counter



def day_timeline(user , df):
    if user != "Overall":
        df = df[df['username'] == user]
    timeline = df.groupby(['day_name']).count()['msg'].reset_index()
    # timeline = df.groupby(['day_order', 'day_name']).count()['msg'].reset_index().drop('day_order',axis='columns')
    # days_dict = {'Monday': 'a' , 'Tuesday': 'b' ,'Wednesday': 'c' ,'Thursday': 'd' ,'Friday': 'e' ,'Saturday': 'f' ,'Sunday': 'g' }
    # timeline['day_order'] = timeline['day_name']
    # timeline['day_order'] = timeline['day_order'].apply(lambda x : days_dict[x])
    # timeline = timeline.sort_values(by='day_order').reset_index()

    fig, ax = plt.subplots()
    plt.xticks(rotation='vertical')
    ax.bar(timeline['day_name'], timeline['msg'], color='r')
    ax.set_ylabel('Message Sent')

    timeline['%Percentage'] = round(100 * timeline['msg'] / timeline['msg'].sum(), 2)
    timeline = timeline.sort_values(by='msg', ascending=False).reset_index()
    return fig , timeline[['day_name' , 'msg' , '%Percentage']].rename(columns={'day_name' : 'Day' , 'msg' : 'Messages Count'})



def monthly_timeline(user , df):
    if user != "Overall":
        df = df[df['username'] == user]


    timeline = df.groupby(['year', 'month_num', 'month']).count()['msg'].reset_index()
    # timeline['months'] =  timeline['month']
    # for i in range(timeline.shape[0]):
    #     timeline['months'][i] += "-" + str(timeline['year'][i])
    timeline['months'] = timeline['month'] + "-" + timeline['year'].astype(str)

    fig, ax = plt.subplots()
    plt.xticks(rotation='vertical')
    ax.bar(timeline['months'], timeline['msg'], color='r')
    ax.set_ylabel('Message Count')

    timeline['%Percentage'] = round(100 * timeline['msg'] / timeline['msg'].sum(), 2)
    timeline = timeline.sort_values(by='msg', ascending=False).reset_index()

    return fig , timeline[['months' , 'msg' , '%Percentage']].rename(columns={'months' : 'Month' , 'msg' : 'Messages Count'})


def yearly_timeline(user , df):
    if user != "Overall":
        df = df[df['username'] == user]
    timeline = df.groupby(['year']).count()['msg'].reset_index()
    fig, ax = plt.subplots()
    plt.xticks(timeline['year'] , rotation='vertical')
    plt.xlabel('Year', fontsize=20)
    ax.bar(timeline['year'], timeline['msg'], color='r')
    ax.set_ylabel('Message Sent')

    timeline['%Percentage'] = round(100 * timeline['msg'] / timeline['msg'].sum(), 2)
    timeline = timeline.sort_values(by='msg', ascending=False).reset_index()
    return fig , timeline[['year' , 'msg' , '%Percentage']].rename(columns={'year' : 'Year' , 'msg' : 'Messages Count'})



def time_period_timeline(user,df):
    if user != "Overall":
        df = df[df['username'] == user]

    pt = df.rename(columns = {'day_name' : 'Days' , 'period':'Hours'}).pivot_table(index=['Days'], columns='Hours', values='msg', aggfunc='count', sort=True).fillna(0)
    fig, ax = plt.subplots()
    ax = sns.heatmap(pt)

    tp_df = df['period'].value_counts().reset_index().rename(columns={'period' : 'Time period(in 24hr_format)' , 'count' : 'Messages Count'})
    return fig , tp_df


def predict_user_preprocess(df):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import make_pipeline
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report

    # Sample data
    messages = df['msg'].tolist()
    labels = df['username'].tolist()
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(messages, labels, test_size=0.2)

    # Create a model pipeline
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())

    # Train the model
    model.fit(X_train, y_train)

    return model.score(X_test , y_test) , model
    # Evaluate the model

    # predicted = model.predict(X_test)

    # print(classification_report(y_test, predicted))

def predict(model , user_input):

    return model.predict([user_input])[0] , max(model.predict_proba([user_input])[0])
