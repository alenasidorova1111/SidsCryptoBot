import requests
import json
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты: {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неверный формат ввода количества валюты: {amount}.')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?base={base_ticker}&symbols={quote_ticker}')
        result = round(json.loads(r.content)['rates'][keys[quote]] * float(amount), 4)
        return result
