import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryproConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start',])
def help(message: telebot.types.Message):
    text = 'Добро пожаловать в Телеграмм Бота по конвертации валюты. Для корректной работы бота посмотрите инструкцию /help'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help',])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу нашего ТГ бота, необходимо ввести команду боту в виде: \n'\
            '<имя валюты, цену которой он хочет узнать> \ ' '<имя валюты, в которой надо узнать цену первой валюты> \ '\
            '<количество первой валюты>''\nПример:''\nдоллар рубль 6''\nЧтобы увидеть список доступных валют, введите команду /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise ConvertionException(f'Слишком много параметров')
        if len(values) < 3:
            raise ConvertionException(f'Слишком мало параметров')
        quote, base, amount = values
        total_base = CryproConverter.get_prace(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду. \n{e}')
    else:
        text = f'Цена за {amount} {quote} в {base} составляет {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
