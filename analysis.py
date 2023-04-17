import pandas as pd
import matplotlib.pyplot as plt
import emoji
import nltk
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')
import string

class color:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Загрузка данных из файла JSON в DataFrame
data = pd.read_json('result.json', encoding='utf-8')

# Преобразование вложенных объектов JSON в отдельные столбцы
df = pd.json_normalize(data['messages'])

message_all = 0
phone_call_all = 0
voice_all = 0
video_mess_all = 0
photo_all = 0
video_all = 0
sticker_all = 0
text_all = 0

# Определение уникальных пользователей и подсчет количества сообщений от каждого пользователя
bebra = {} # Создаем пустой словарь для хранения количества сообщений каждого пользователя
for user in df['from'].dropna().unique():
    print(emoji.emojize(':person:'), color.BOLD + user + ':' + color.END)

    # Подсчет количества сообщений от каждого пользователя
    user_message_count = df['from'].value_counts()[user]
    bebra[user] = user_message_count
    message_all += user_message_count
    print(emoji.emojize(':envelope:'), f' Сообщений: {user_message_count}')

    # Подсчет количества звонков от каждого пользователя
    user_call_count = df[(df['action'] == 'phone_call') & (df['actor'] == user)].shape[0]
    phone_call_all += user_call_count
    print(emoji.emojize(':telephone_receiver:'), f'Звонков: {user_call_count}')

    # Подсчет голосовых сообщений от каждого пользователя
    voice = df[(df['media_type'] == 'voice_message') & (df['from'] == user)].shape[0]
    voice_all += voice
    print(emoji.emojize(':microphone:'), f'Голосовых: {voice}')

    # Подсчет видеосообщений от каждого пользователя
    video_mess = df[(df['media_type'] == 'video_message') & (df['from'] == user)].shape[0]
    video_mess_all += video_mess
    print(emoji.emojize(':movie_camera:'), f'Видеосообщений: {video_mess}')

    # Подсчет фотографий от каждого пользователя
    photo = df[(df['photo'] == '(File not included. Change data exporting settings to download.)') & (df['from'] == user)].shape[0]
    photo_all += photo
    print(emoji.emojize(':camera:'), f'Фотографий: {photo}')

    # Подсчет видео от каждого пользователя
    video = df[(df['media_type'] == 'video_file') & (df['from'] == user)].shape[0]
    video_all += video
    print(emoji.emojize(':clapper_board:'), f'Видео: {video}')

    # Подсчет стикеров от каждого пользователя
    sticker = df[(df['media_type'] == 'sticker') & (df['from'] == user)].shape[0]
    sticker_all += sticker
    print(emoji.emojize(':performing_arts:'), f'Стикеров: {sticker}')

    print('________________________')

text_all = message_all - voice_all - video_mess_all - photo_all - video_all - sticker_all

print(emoji.emojize(':envelope:'), ' Всего сообщений:', message_all)
print(emoji.emojize(':telephone_receiver:'), 'Всего звонков:', phone_call_all)
print(emoji.emojize(':microphone:'), 'Всего голосовых сообщений:', voice_all)
print(emoji.emojize(':movie_camera:'), 'Всего видеосообщений:', video_mess_all)
print(emoji.emojize(':camera:'), 'Всего фотографий:', photo_all)
print(emoji.emojize(':clapper_board:'), 'Всего видео:', video_all)
print(emoji.emojize(':performing_arts:'), 'Всего стикеров:', sticker_all)
print(emoji.emojize(':pencil:'), ' Всего текстовых сообщений:', text_all)

df_lengths = df['text'].map(len)
mean_lengths = df_lengths.mean()
print(emoji.emojize(':balance_scale:'), ' Средняя длина текстового сообщения:', round(mean_lengths))

def bar_chart(df):
    # выделить месяцы сообщений
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.strftime('%Y-%m')

    # создать DataFrame с месяцами и количеством сообщений за каждый месяц
    month_counts = df.groupby('month').size().reset_index(name='count')

    # пересоздать индекс DataFrame с ежемесячным интервалом дат
    start_date = pd.to_datetime(month_counts['month'].min() + '-01')
    end_date = pd.to_datetime(month_counts['month'].max() + '-01') + pd.offsets.MonthEnd(1)
    monthly_index = pd.date_range(start=start_date, end=end_date, freq='MS').strftime('%Y-%m')
    month_counts = month_counts.set_index('month').reindex(monthly_index, fill_value=0)

    # построение гистограммы с окантовкой и перекраской столбиков
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.bar(month_counts.index, month_counts['count'], width=1, color='blue', edgecolor='black')
    ax.set_xlabel('Date')
    ax.set_ylabel('Count')
    ax.set_title('Number of messages per month')
    ax.set_xticklabels(month_counts.index, rotation=70)
    plt.savefig('image/my_bar_chart.png', dpi=300, bbox_inches='tight')
    most_active_month = month_counts.loc[month_counts['count'].idxmax()]
    print(emoji.emojize(':TOP_arrow:'), 'В самый активный месяц', most_active_month.name, 'было отправлено', month_counts['count'].max(), 'соообщения')

def pie_chart(bebra):
    sizes = []
    labels = []

    for i in bebra:
        sizes.append(bebra[i])
        labels.append(i)

    # создание кругового графика
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # для того, чтобы круг был кругом

    # добавление заголовка
    plt.title('Соотношение количества сообщений')

    # экспортирование графика в файл png
    plt.savefig('image/my_pie_chart.png', dpi=300, bbox_inches='tight')

def pie_chart_mess(sticker_all, video_all, photo_all, video_mess_all, voice_all, phone_call_all, text_all):
    sizes = [sticker_all, video_all, photo_all, video_mess_all, voice_all, phone_call_all, text_all]
    labels = ['стикеры', 'видео', 'фото', 'видеосообщения', 'голосовые сообщения', 'звонки', 'текстовые сообщения']

    # создание кругового графика
    fig1, ax1 = plt.subplots(figsize=(16, 9))
    ax1.pie(sizes, labels=None, startangle=90)

    # добавление легенды снизу
    ax1.legend(labels, loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=len(labels))

    # добавление заголовка
    plt.title('Отношение каждого вида сообщений')

    # экспортирование графика в файл png
    plt.savefig('image/my_pie_chart_2.png', dpi=500, bbox_inches='tight')

#частота встречаимости слов в сообщениях
def word_frequency(df):
    #создание списка текста в сообщениях
    text_list = list(df['text'])
    #переводим список в строку
    string_elements = [elem for elem in text_list if isinstance(elem, str)]
    sentence_example = ' '.join(string_elements)
    #создаем список токенов
    tokens = word_tokenize(sentence_example, language="russian")

    russian_stop_words = stopwords.words("russian")

    #удаление пунктуации
    tokens = [i for i in tokens if i not in string.punctuation]
    #удаление стоп-слов и коротких слов(местоимения, междометия, союзы), переводим всё в нижний регистр
    tokens = [i.lower() for i in tokens if i not in russian_stop_words and len(i) >= 4]
    mySeries = pd.Series(tokens)

    print(mySeries.value_counts())


bar_chart(df)
pie_chart(bebra)
pie_chart_mess(sticker_all, video_all, photo_all, video_mess_all, voice_all, phone_call_all, text_all)
word_frequency(df)

print ('Готово')
