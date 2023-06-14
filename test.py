import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token.txt')
UPLOADS_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'json file download')

with open(API_TOKEN_FILE, encoding='utf-8') as f:
    for line in f:
        token = line

# Инициализация бота
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Включаем логирование
logging.basicConfig(level=logging.INFO)

def parse_imgs():
    imgs = []
    for img in os.listdir(UPLOADS_DIRECTORY):
        imgs.append(types.InputMediaPhoto(open(os.path.join(UPLOADS_DIRECTORY, img), 'rb')))
    return imgs

async def delete_file_delayed(file_path, delay):
    await asyncio.sleep(delay)
    os.remove(file_path)
    loop.remove_signal_handler(asyncio.current_task())

# Хендлер для начала работы с ботом
@dp.message_handler(commands='start')
async def start_mess(message: types.Message):
    await message.answer("Привет! Это проект ASMT.")
    mess = "Я бот-анализатор, и для моей работы нужен json-файл\n На скриншотах представлена инструкция как это сделать."
    await message.answer(mess)
    imgs = parse_imgs()
    await bot.send_media_group(message.chat.id, media=imgs)

# Хендлер для загрузки документа
@dp.message_handler(content_types=['document'])
async def handle_docs(message: types.Message):
    # try:
    chat_id = message.chat.id

    file_info = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), message.document.file_name)
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file.read())

    await message.reply("Пожалуй, я сохраню это")
    
    loop = asyncio.get_running_loop()
    file_to_delete = os.path.join(os.getcwd(), src)
    loop.create_task(delete_file_delayed(src, 10))
# except Exception as e:
    #     await message.reply(str(e))

@dp.message_handler()
async def cannot_do_command(message: types.Message):
    await message.answer("Извини, не понимаю твоей команды")

async def start_bot():
    await dp.start_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    loop.run_forever()