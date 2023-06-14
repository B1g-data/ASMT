import telebot
import os


with open(f'{os.path.dirname(os.path.abspath(__file__))}\\token.txt', 'r', encoding='utf-8') as f:
    for line in f:
        token = line


bot = telebot.TeleBot(token)

def pr(chat_id):
    bot.send_message(chat_id, "Kon'")

def parse_imgs():
    imgs = []
    path = os.path.dirname(os.path.abspath(__file__))+'\\json file download'
    for img in os.listdir(path):
        imgs.append(telebot.types.InputMediaPhoto(open(path+f'\\{img}', 'rb')))
    return(imgs)


download_imgs = parse_imgs()
#Хендлер для начала работы с ботом    
@bot.message_handler(commands='start')
def start_mess(message):
    bot.send_message(message.chat.id, "Привет! Это проект ASMT.")
    mess = "Я бот-анализатор, и для моей работы нужен json-файл\n На скриншотах представлена инструкция как это сделать."
    bot.send_message(message.chat.id, mess)
    imgs = download_imgs
    bot.send_media_group(message.chat.id, media=imgs)

#Хендлер для вывода расписания

@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = os.path.dirname(os.path.abspath(__file__))+ '\\download' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Пожалуй, я сохраню это")
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler()
def cannot_do_comand(message):
    bot.send_message(message.chat.id, "Извини не понимаю твоей команды")
#@bot.message_handler(commands='сравнение')
#def compare(message):

bot.polling(non_stop=True)
