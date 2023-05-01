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



#Хендлер для начала работы с ботом    
@bot.message_handler(commands='start')
def start_mess(message):
    bot.send_message(message.chat.id, "Привет! Это проект ASMT.")
    mess = "Я бот-анализатор, и для моей работы нужен json-файл\n На скриншотах представлена инструкция как это сделать."
    bot.send_message(message.chat.id, mess)
    imgs = parse_imgs()
    bot.send_media_group(message.chat.id, media=imgs)

#Хендлер для вывода расписания


#@bot.message_handler(commands='сравнение')
#def compare(message):

bot.polling(non_stop=True)
