import telebot
import requests.exceptions
from extensions import *
from config import TOKEN, CURRENCY_KEYS


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handler_start_help(message: telebot.types.Message):
    if message.text == '/start':
        bot.send_message(
            message.chat.id,
            f'Приветствую,  {message.chat.username}!\n\n'
            'Получить список доступных валют, команда: /values\n\n'
            'Конвертировать валюту, команда: доллар евро 10\n'
            'Конвертирует 10 долларов в евро.'
        )
    else:
        bot.send_message(
            message.chat.id,
            'Получить список доступных валют, команда: /values\n\n'
            'Конвертировать валюту, команда: доллар евро 10\n'
            'Конвертирует 10 долларов в евро.'
        )


@bot.message_handler(commands=['values'])
def handler_values(message: telebot.types.Message):
    text = 'Список доступных валют:\n'
    for key in CURRENCY_KEYS.keys():
        text += f'    {key}\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def handler_any_text(message: telebot.types.Message):
    message_user = message.text.lower().split()
    try:
        if len(message_user) == 3:
            base_currency, quote_currency, base_amount = message_user
        else:
            raise BotExceptionToManyAttr()

        if not base_currency.isalpha() or not quote_currency.isalpha():
            raise BotExceptionToManyAttr()

        if base_currency == quote_currency:
            raise BotExceptionEqCurrency()

        if {base_currency, quote_currency}.issubset(CURRENCY_KEYS.keys()):
            base_ticker = CURRENCY_KEYS[base_currency]
            quote_ticker = CURRENCY_KEYS[quote_currency]
        else:
            raise BotExceptionNotSupportCurrency()

        base_amount = base_amount.replace(',', '.', 1)

        if not base_amount.replace('.', '', 1).isdigit():
            raise BotExceptionAttrNotFloat()
        base_amount = float(base_amount)

        quote_amount = ExchangeCurrency.get_price(
            base_ticker, quote_ticker, base_amount
        )

    except BotException as error:
        bot.send_message(message.chat.id, f'Ошибка:\n    {error}\n')
    except requests.RequestException:
        bot.send_message(message.chat.id, f'Ошибка сервера:\n'
                                          f'    Повторите позже.\n'
                         )

    else:
        bot.send_message(message.chat.id,
                         f'{base_amount:.2f} {base_currency} '
                         f'равно {quote_amount:.2f} {quote_currency}'
                         )


# bot.polling(none_stop=True)
bot.infinity_polling()
