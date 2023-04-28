import string
import pandas as pd
import matplotlib.pyplot as plt
import emoji
import nltk
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')


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
users = df['from'].dropna().unique()

#статистика по юзерам
def user_statistic(user):
    global message_all, phone_call_all, voice_all, video_mess_all, photo_all, video_all, sticker_all, text_all

    # Подсчет количества сообщений от каждого пользователя
    user_message_count = df['from'].value_counts()[user]
    bebra[user] = user_message_count
    message_all += user_message_count

    # Подсчет количества звонков от каждого пользователя
    user_call_count = df[(df['action'] == 'phone_call') &
                         (df['actor'] == user)].shape[0]
    phone_call_all += user_call_count

    # Подсчет голосовых сообщений от каждого пользователя
    voice = df[(df['media_type'] == 'voice_message')
               & (df['from'] == user)].shape[0]
    voice_all += voice

    # Подсчет видеосообщений от каждого пользователя
    video_mess = df[(df['media_type'] == 'video_message')
                    & (df['from'] == user)].shape[0]
    video_mess_all += video_mess

    # Подсчет фотографий от каждого пользователя
    photo = df[(df['photo'] == '(File not included. Change data exporting settings to download.)') & (
        df['from'] == user)].shape[0]
    photo_all += photo

    # Подсчет видео от каждого пользователя
    video = df[(df['media_type'] == 'video_file')
               & (df['from'] == user)].shape[0]
    video_all += video

    # Подсчет стикеров от каждого пользователя
    sticker = df[(df['media_type'] == 'sticker')
                 & (df['from'] == user)].shape[0]
    sticker_all += sticker

    return f"{emoji.emojize(':person:')} {color.BOLD + user + ':' + color.END}\n\
{emoji.emojize(':envelope:')}  Сообщений: {user_message_count}\n\
{emoji.emojize(':telephone_receiver:')} Звонков: {user_call_count}\n\
{emoji.emojize(':microphone:')} Голосовых: {voice}\n\
{emoji.emojize(':movie_camera:')} Видеосообщений: {video_mess}\n\
{emoji.emojize(':camera:')} Фотографий: {photo}\n\
{emoji.emojize(':clapper_board:')} Видео: {video}\n\
{emoji.emojize(':performing_arts:')} Стикеров: {sticker}\n"

#общая статистика
def statistic_all():
    global text_all
    text_all = message_all - voice_all - video_mess_all - \
        photo_all - video_all - sticker_all
    df_lengths = df['text'].map(len)
    mean_lengths = df_lengths.mean()

    return f"{emoji.emojize(':bar_chart:')} {color.BOLD + 'Общая статистика:' + color.END}\n\
{emoji.emojize(':envelope:')}  Всего сообщений: {message_all}\n\
{emoji.emojize(':telephone_receiver:')} Всего звонков: {phone_call_all}\n\
{emoji.emojize(':microphone:')} Всего голосовых сообщений: {voice_all}\n\
{emoji.emojize(':movie_camera:')} Всего видеосообщений: {video_mess_all}\n\
{emoji.emojize(':camera:')} Всего фотографий: {photo_all}\n\
{emoji.emojize(':clapper_board:')} Всего видео: {video_all}\n\
{emoji.emojize(':performing_arts:')} Всего стикеров: {sticker_all}\n\
{emoji.emojize(':pencil:')}  Всего текстовых сообщений: {text_all}\n\
{emoji.emojize(':balance_scale:')}  Средняя длина текстового сообщения: {round(mean_lengths)}"

#гистограмма распределения сообщений по месяцам
def bar_chart():
    global df
    # выделить месяцы сообщений
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.strftime('%Y-%m')

    # создать DataFrame с месяцами и количеством сообщений за каждый месяц
    month_counts = df.groupby('month').size().reset_index(name='count')

    # пересоздать индекс DataFrame с ежемесячным интервалом дат
    start_date = pd.to_datetime(month_counts['month'].min() + '-01')
    end_date = pd.to_datetime(
        month_counts['month'].max() + '-01') + pd.offsets.MonthEnd(1)
    monthly_index = pd.date_range(
        start=start_date, end=end_date, freq='MS').strftime('%Y-%m')
    month_counts = month_counts.set_index(
        'month').reindex(monthly_index, fill_value=0)

    # построение гистограммы с окантовкой и перекраской столбиков
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.bar(month_counts.index,
           month_counts['count'], width=1, color='blue', edgecolor='black')
    ax.set_xlabel('Date')
    ax.set_ylabel('Count')
    ax.set_title('Number of messages per month')
    ax.set_xticklabels(month_counts.index, rotation=70)
    plt.savefig('image/my_bar_chart.png', dpi=300, bbox_inches='tight')
    most_active_month = month_counts.loc[month_counts['count'].idxmax()]
    print(emoji.emojize(':TOP_arrow:'), 'В самый активный месяц', most_active_month.name,
          'было отправлено', month_counts['count'].max(), 'соообщения')

#круговая диаграмма по количеству сообщений от юзеров
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

#круговая диаграмма соотношений по виду сообщений#
def pie_chart_mess():
    global message_all, phone_call_all, voice_all, video_mess_all, photo_all, video_all, sticker_all, text_all
    sizes = [sticker_all, video_all, photo_all,
             video_mess_all, voice_all, phone_call_all, text_all]
    labels = ['стикеры', 'видео', 'фото', 'видеосообщения',
              'голосовые сообщения', 'звонки', 'текстовые сообщения']

    # создание кругового графика
    fig1, ax1 = plt.subplots(figsize=(16, 9))
    ax1.pie(sizes, labels=None, startangle=90)

    # добавление легенды снизу
    ax1.legend(labels, loc='lower center',
               bbox_to_anchor=(0.5, -0.25), ncol=len(labels))

    # добавление заголовка
    plt.title('Отношение каждого вида сообщений')

    # экспортирование графика в файл png
    plt.savefig('image/my_pie_chart_2.png', dpi=500, bbox_inches='tight')

# частота встречаимости слов в сообщениях
def word_frequency():
    global df
    # создание списка текста в сообщениях
    text_list = list(df['text'])
    # переводим список в строку
    string_elements = [elem for elem in text_list if isinstance(elem, str)]
    sentence_example = ' '.join(string_elements)
    # создаем список токенов
    tokens = word_tokenize(sentence_example, language="russian")

    russian_stop_words = stopwords.words("russian")

    # удаление пунктуации
    tokens = [i for i in tokens if i not in string.punctuation]
    # удаление стоп-слов и коротких слов(местоимения, междометия, союзы), переводим всё в нижний регистр
    tokens = [i.lower()
              for i in tokens if i not in russian_stop_words and len(i) >= 4]
    mySeries = pd.Series(tokens)

    return(mySeries.value_counts())

if __name__ == "__main__":
    # Определение уникальных пользователей и подсчет количества сообщений от каждого пользователя
    bebra = {}  # Создаем пустой словарь для хранения количества сообщений каждого пользователя
    for user in df['from'].dropna().unique():
        print(user_statistic(user))

    print(statistic_all())

    bar_chart()

    pie_chart(bebra)

    pie_chart_mess()
    
    print(word_frequency())

    print('Готово')