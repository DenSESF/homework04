"""
Настройки бота
TOKEN - токен бота телеграм
API_ID - токен для доступа к api на сайте https://openexchangerates.org/
URL - ссылка для вызова API
CURRENCY_KEYS - настройка списка валют
RATES_BUFFER - буфер для курсов валют на сутки, что бы уменьшить обращения к API
               значение 'file' - сохраняет локально в файл currency_rates.json
               значение 'redis' - сохраняет на сервере redis
               значение None - не использовать буфер
REDIS_SRV - адрес сервера redis
REDIS_PORT - порт сервера
REDIS_PASS - пароль для доступа к серверу
"""
TOKEN = 'токен телеграм бота'

API_ID = 'api id'
URL = 'https://openexchangerates.org/api/latest.json?app_id='

CURRENCY_KEYS = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB'
}

RATES_BUFFER = None

REDIS_SRV = 'cloud.redislabs.com'
REDIS_PORT = 12345
REDIS_PASS = 'пароль'
