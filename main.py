import telebot
from telebot import types

try:
    import xml.etree.cElementTree as ET
except ImportError:  # Запретное заклятие для более быстрой работы XML
    import xml.etree.ElementTree as ET

import weather

list_tokens = []


def read_tokens(file_tokens="tokens.xml"):
    """Чтение XML файла с токенами"""

    cur_time_session = ET.parse(f"{file_tokens}").getroot()

    if len(list_tokens) == 0:
        for one_token in cur_time_session.findall("token"):
            token = (one_token.attrib["id"], one_token.attrib["name"], str(one_token[0].text))
            list_tokens.append(token)
    else:
        list_tokens.clear()
        read_tokens()


name = 'Aisberg_D_bot'
read_tokens()
bot = telebot.TeleBot(list_tokens[0][2])
standart_ansver = 'Я не знаю, что ответить на: '

@bot.message_handler(commands=['start'])
def keyboard(message):
    print('Ввведена привественная команда для начала беседы:')

    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(
            text='Узнать актуальную ситуацию по короновирусу',
            callback_data='coronovirus_callback_data'
        ),
        types.InlineKeyboardButton(
            text='Узнать текущую погоду',
            callback_data='weather_callback_data'
        ),
        types.InlineKeyboardButton(
            text='Хочу связаться с создателем бота',
            url='aisberg.d@inbox.ru'
        )
    ]
    markup.add(*buttons)
    bot.send_message(message.chat.id, 'Приветствую! С чем пожаловали?', reply_markup=markup)

@bot.message_handler(commands=["geo"])
def geo(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку и передай мне свое местоположение", reply_markup=keyboard)

@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        print(message.location)
        print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))


# @bot.message_handler(commands=['button'])
# def button_message(message):
#     markup=types.InlineKeyboardMarkup(row_width=1)
#     button_weather=types.KeyboardButton("Погода", callback_data='погода')
#     markup.add(button_weather)
#     bot.send_message(message.chat.id,'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def check_messages(message):
    print(f'Получено от {message.chat.id}: {message.text}')
    answer = f'Я не знаю, что ответить на: {message.text}'
    if "погода" in message.text.lower():
        answer = weather.get_weather(weather.city_name)
    elif "привет" or "здравствуй" in message.text.lower():
        answer = "Приветствую! Для удобства используйте команду: /start"
    else:
        bot.send_message(message.chat.id, standart_ansver)
    bot.send_message(message.chat.id, answer)
    print(f'Отвечено {message.chat.id}: {answer}')

if __name__ == '__main__':
     #token = '1776121319:AAGsSuOnY3OxRq4vYOTWDkIm46C9UOD22oo'
     print('Ща включусь!')
     bot.infinity_polling()




