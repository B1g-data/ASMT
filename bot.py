import telebot


with open('token.txt', 'r', encoding='utf-8') as f:
    for line in f:
        token = line


bot = telebot.TeleBot(token)

def pr(chat_id):
    bot.send_message(chat_id, "Kon'")

#Хендлер для начала работы с ботом    
@bot.message_handler(commands='start')
def start_mess(message):
    bot.send_message(message.chat.id, "Привет! Это проект ASMT.")
    mess = "Я бот-анализатор, и для моей работы нужен json-файл\n На скриншотах представлена инструкция как это сделать."
    bot.send_message(message.chat.id, mess)
    bot.send_photo(message.chat.id, photo=open('photo/pic_1.png', 'rb'))

#Хендлер для вывода расписания


#@bot.message_handler(commands='сравнение')
#def compare(message):

bot.polling(non_stop=True)