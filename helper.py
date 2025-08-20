from urlextract import URLExtract
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import re
extractor = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_common_words(selected_user, df):
    # Filter user-specific data if not overall
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Load stopwords
    with open("assets/stopwords.txt", "r", encoding="utf-8") as f:
        stop_words = set(f.read().splitlines())

    # Remove null, blank, and media omitted messages
    temp = df[(df['message'].notna()) &
              (df['message'].str.strip() != '') &
              (df['message'] != '<Media omitted>')]

    words = []

    for message in temp['message']:
        # Remove URLs, numbers, emojis, and special characters
        message = re.sub(r'http\S+|www\S+', '', message)  # Remove links
        message = re.sub(r'[^a-zA-Z\s]', '', message)  # Keep only alphabets
        for word in message.lower().split():
            if word and word not in stop_words:  # Skip empty words & stopwords
                words.append(word)

    # Count top 20 words
    most_common = Counter(words).most_common(20)
    return pd.DataFrame(most_common, columns=['Word', 'Count'])


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['message'] != '<Media omitted>']
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    return wc.generate(temp['message'].str.cat(sep=" "))


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby([df['year'], df['month']]).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + " " + timeline['year'].astype(str)
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('date').count()['message'].reset_index()
    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()
