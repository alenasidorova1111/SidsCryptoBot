import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = 'Чтобы начать работу отправьте сообщение с тремя параметрами (через пробел) в следующем формате: \n <Имя ' \
           'конвертируемой валюты><имя валюты, в которую конвертируем><количество конвертируемой валюты>\n Например: ' \
           '"доллар евро 10"\n\n Чтобы увидеть список всех доступных валют введите команду: /values '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        parameters = message.text.split(' ')

        if len(parameters) != 3:
            raise APIException('Количество параметров не соответствует необходимому. Необходимо ввести 3 параметра.')

        base, quote, amount = parameters
        total_base = CryptoConverter.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду. \n{e}')
    else:
        text = f'Цена {amount} {base} в {quote}: {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
