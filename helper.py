# from collections import Counter
# import pandas as pd
# from urlextract import URLExtract
# extract = URLExtract()
# from wordcloud import WordCloud
# import emoji


# def fetch_stats(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     num_messages = df.shape[0]
#     words = []
#     for message in df['message']:
#         words.extend(message.split())

#     # fetch no of media messages
#     num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

#     # fetch number of links shared
#     links = []
#     for message in df['message']:
#         links.extend(extract.find_urls(message))

#     return num_messages, len(words),num_media_messages,len(links)



# def fetch_most_busy_users(df):
#     x = df['user'].value_counts().head()
#     # not getting correct output
#     df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
#         columns={'index': 'name', 'user': 'percent'})
#     return x,df

# def create_wordcloud(selected_user,df):
#     f = open('stop_hinglish.txt', 'r')
#     stop_words = f.read()

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     temp = df[df['user'] != 'group_notification']
#     temp = temp[temp['message'] != '<Media omitted>\n']

#     def remove_stopwords(message):
#         y = []
#         for word in message.lower().split():
#             if word not in stop_words:
#                 y.append(word)
#         return " ".join(y)


#     wc = WordCloud(width=800, height=800, background_color='white')
#     temp['message'] = temp['message'].apply(remove_stopwords)
#     df_wc = wc.generate(temp['message'].str.cat(sep=" "))
#     return df_wc

# def most_common_words(selected_user,df):
#     f = open('stop_hinglish.txt', 'r')
#     stop_words = f.read()

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     temp = df[df['user'] != 'group_notification']
#     temp = temp[temp['message'] != '<Media omitted>\n']

#     words = []

#     for message in temp['message']:
#         for word in message.lower().split():
#             if word not in stop_words:
#                 words.append(word)
#         words.extend(message.split())

#     most_common_df = pd.DataFrame(Counter(words).most_common(20))
#     return most_common_df

# def emoji_helper(selected_user, df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     emojis = []

#     for message in df['message']:
#         for c in message:
#             if emoji.is_emoji(c):
#                 emojis.append(c)

#     emoji_df = pd.DataFrame(Counter(emojis).most_common())

#     return emoji_df

# def monthly_timeline(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

#     time = []
#     for i in range(timeline.shape[0]):
#         time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

#     timeline['time'] = time
#     return timeline

# def daily_timeline(selected_user,df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     daily_timeline = df.groupby('only_date').count()['message'].reset_index()

#     return daily_timeline

# def week_activity_map(selected_user,df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     return df['day_name'].value_counts()

# def month_activity_map(selected_user,df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     return df['month'].value_counts()

# def activity_heatmap(selected_user,df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

#     return user_heatmap




############################################## NEW HELPER CODE ######################################################
from collections import Counter

import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
import emoji


# ---------------------------------------------------------
# URL extractor
# ---------------------------------------------------------

extract = URLExtract()


# ---------------------------------------------------------
# Constants
# ---------------------------------------------------------

MEDIA_MESSAGE = '<Media omitted>'
GROUP_NOTIFICATION = 'group_notification'


# ---------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------

def filter_user(selected_user, df):
    """
    Return data for the selected user.

    If 'Overall' is selected, return the complete DataFrame.
    """

    if selected_user != 'Overall':
        return df[df['user'] == selected_user].copy()

    return df.copy()


def get_stop_words():
    """
    Load Hinglish stop words into a set.

    Using a set makes stop-word lookup much faster than
    searching through a single string.
    """

    try:
        with open(
            'stop_hinglish.txt',
            'r',
            encoding='utf-8'
        ) as f:

            stop_words = {
                word.strip().lower()
                for word in f
                if word.strip()
            }

        return stop_words

    except FileNotFoundError:
        return set()


# ---------------------------------------------------------
# BASIC CHAT STATISTICS
# ---------------------------------------------------------

def fetch_stats(selected_user, df):

    df = filter_user(selected_user, df)

    # Number of messages
    num_messages = df.shape[0]

    # Number of words
    words = []

    for message in df['message']:
        words.extend(str(message).split())

    # Number of media messages
    num_media_messages = (
        df['message']
        .astype(str)
        .str.strip()
        .eq(MEDIA_MESSAGE)
        .sum()
    )

    # Number of links
    links = []

    for message in df['message']:
        links.extend(
            extract.find_urls(str(message))
        )

    return (
        num_messages,
        len(words),
        num_media_messages,
        len(links)
    )


# ---------------------------------------------------------
# MOST ACTIVE USERS
# ---------------------------------------------------------

def fetch_most_busy_users(df):

    # Number of messages per user
    x = df['user'].value_counts().head()

    # Percentage contribution
    user_percentage = (
        df['user']
        .value_counts(normalize=True)
        .mul(100)
        .round(2)
        .reset_index()
    )

    user_percentage.columns = [
        'name',
        'percent'
    ]

    return x, user_percentage


# ---------------------------------------------------------
# WORD CLOUD
# ---------------------------------------------------------

def create_wordcloud(selected_user, df):

    df = filter_user(selected_user, df)

    # Remove group notifications
    temp = df[
        df['user'] != GROUP_NOTIFICATION
    ].copy()

    # Remove media messages
    temp = temp[
        temp['message']
        .astype(str)
        .str.strip()
        != MEDIA_MESSAGE
    ]

    # Handle empty data
    if temp.empty:
        return None

    stop_words = get_stop_words()

    def remove_stopwords(message):

        words = []

        for word in str(message).lower().split():

            # Remove punctuation around words
            clean_word = word.strip(
                '.,!?;:"\'()[]{}'
            )

            if clean_word and clean_word not in stop_words:
                words.append(clean_word)

        return " ".join(words)

    temp['message'] = temp['message'].apply(
        remove_stopwords
    )

    text = temp['message'].str.cat(
        sep=" "
    ).strip()

    if not text:
        return None

    wc = WordCloud(
        width=800,
        height=800,
        background_color='white'
    )

    return wc.generate(text)


# ---------------------------------------------------------
# MOST COMMON WORDS
# ---------------------------------------------------------
def most_common_words(selected_user, df):

    df = filter_user(selected_user, df)

    # Remove group notifications
    temp = df[
        df['user'] != GROUP_NOTIFICATION
    ].copy()

    # Remove media messages
    temp = temp[
        temp['message']
        .astype(str)
        .str.strip()
        != MEDIA_MESSAGE
    ]

    stop_words = get_stop_words()

    words = []

    for message in temp['message']:

        for word in str(message).lower().split():

            # Remove basic punctuation
            clean_word = word.strip(
                '.,!?;:"\'()[]{}'
            )

            if (
                clean_word
                and clean_word not in stop_words
            ):
                words.append(clean_word)

    # IMPORTANT:
    # This must be OUTSIDE the for loops
    most_common_df = pd.DataFrame(
        Counter(words).most_common(20),
        columns=[0, 1]
    )

    return most_common_df


# ---------------------------------------------------------
# EMOJI ANALYSIS
# ---------------------------------------------------------
def emoji_helper(selected_user, df):

    df = filter_user(selected_user, df)

    emojis = []

    for message in df['message']:

        for character in str(message):

            if emoji.is_emoji(character):
                emojis.append(character)

    emoji_df = pd.DataFrame(
        Counter(emojis).most_common()
    )

    return emoji_df

# ---------------------------------------------------------
# MONTHLY TIMELINE
# ---------------------------------------------------------

def monthly_timeline(selected_user, df):

    df = filter_user(selected_user, df)

    timeline = (
        df.groupby(
            ['year', 'month_num', 'month']
        )
        .count()['message']
        .reset_index()
    )

    # Sort chronologically
    timeline = timeline.sort_values(
        ['year', 'month_num']
    ).reset_index(drop=True)

    timeline['time'] = (
        timeline['month']
        + "-"
        + timeline['year'].astype(str)
    )

    return timeline


# ---------------------------------------------------------
# DAILY TIMELINE
# ---------------------------------------------------------

def daily_timeline(selected_user, df):

    df = filter_user(selected_user, df)

    daily = (
        df.groupby('only_date')
        .count()['message']
        .reset_index()
    )

    return daily


# ---------------------------------------------------------
# WEEKDAY ACTIVITY
# ---------------------------------------------------------

def week_activity_map(selected_user, df):

    df = filter_user(selected_user, df)

    return df['day_name'].value_counts()


# ---------------------------------------------------------
# MONTH ACTIVITY
# ---------------------------------------------------------

def month_activity_map(selected_user, df):

    df = filter_user(selected_user, df)

    return df['month'].value_counts()


# ---------------------------------------------------------
# ACTIVITY HEATMAP
# ---------------------------------------------------------

def activity_heatmap(selected_user, df):

    df = filter_user(selected_user, df)

    user_heatmap = (
        df.pivot_table(
            index='day_name',
            columns='period',
            values='message',
            aggfunc='count'
        )
        .fillna(0)
    )

    return user_heatmap