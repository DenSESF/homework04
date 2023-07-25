import requests
import redis
import json
import os.path
from config import API_ID, URL, CURRENCY_KEYS, RATES_BUFFER, REDIS_SRV, REDIS_PORT, REDIS_PASS
from datetime import date


class BotException(Exception):
    pass


class BotExceptionToManyAttr(BotException):
    def __str__(self):
        return 'Неправильный формат запроса!\n' \
               '    Наберите команду /help для справки.'


class BotExceptionEqCurrency(BotException):
    def __str__(self):
        return 'Конвертация одинаковых валют невозможна!\n' \
               '    Наберите команду /help для справки.'


class BotExceptionNotSupportCurrency(BotException):
    def __str__(self):
        return 'Валюта не поддерживается!\n' \
               '    Наберите команду /values для просмотра ' \
               'списка доступных валют.'


class BotExceptionAttrNotFloat(BotException):
    def __str__(self):
        return 'Укажите количество валюты в виде цифр!\n' \
               '    Например: 10,50 или 10.50 или 10.'


class ExchangeCurrency:

    @staticmethod
    def buffer_rates(rates_dict):
        buffer_dict = rates_dict
        if rates_dict is not None and RATES_BUFFER == 'file':
            data = {'date': str(date.today()), 'currency': rates_dict}
            with open('currency_rates.json', 'w', encoding='utf-8') as file_buffer:
                json.dump(data, file_buffer, indent=4)
            return rates_dict

        elif rates_dict is not None and RATES_BUFFER == 'redis':
            redis_db = redis.Redis(REDIS_SRV, port=REDIS_PORT, password=REDIS_PASS)
            data = {'date': str(date.today()), 'currency': rates_dict}
            redis_db.set('buffer', json.dumps(data))
            return rates_dict

        if os.path.isfile('currency_rates.json') and RATES_BUFFER == 'file':
            with open("currency_rates.json", "r") as file_buffer:
                json_data = json.load(file_buffer)
            if json_data['date'] != str(date.today()):
                buffer_dict = None
            else:
                buffer_dict = json_data['currency'].copy()

        elif RATES_BUFFER == 'redis':
            redis_db = redis.Redis(REDIS_SRV, port=REDIS_PORT, password=REDIS_PASS)
            data = redis_db.get('buffer')
            if data:
                json_data = json.loads(data)
                if json_data['date'] != str(date.today()):
                    buffer_dict = None
                else:
                    buffer_dict = json_data['currency'].copy()

        return buffer_dict

    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:

        def connect_exchange_api(buffer_rate):
            if buffer_rate is None:
                temp_dict = {}
                headers = {"accept": "application/json"}
                response = requests.get(f'{URL}{API_ID}', headers=headers)
                response_dict = json.loads(response.content)

                for val in CURRENCY_KEYS.values():
                    temp_dict[val] = response_dict['rates'][val]

                return ExchangeCurrency.buffer_rates(temp_dict)
            else:
                return buffer_rate

        rates_dict = connect_exchange_api(ExchangeCurrency.buffer_rates(None))

        target_amount = None
        if base == 'USD' and quote in {'EUR', 'RUB'}:
            target_amount = amount * rates_dict[quote]

        elif base in {'EUR', 'RUB'} and quote == 'USD':
            target_amount = amount / rates_dict[base]

        elif base in {'EUR', 'RUB'} and quote in {'EUR', 'RUB'}:
            target_amount = amount / (rates_dict[base] / rates_dict[quote])

        return target_amount
