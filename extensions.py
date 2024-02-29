import json
import requests
from config import keys


class ConvertionException(Exception):
    pass

class CryproConverter:
    @staticmethod
    def get_prace(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException (f'Не удалость обработать валюту {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException (f'Не удалость обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException (f'Не удалость обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base * amount
