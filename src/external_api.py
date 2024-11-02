import os

import requests
from dotenv import load_dotenv

from src.transaction_parser import load_user_settings

# Загружаем переменные окружения из .env файла
load_dotenv()
CURRENCY_LAYER_API_KEY = os.getenv('CURRENCY_LAYER_API_KEY')


def get_currency_rates():
    settings = load_user_settings()
    user_currencies = settings.get("user_currencies", [])

    if not user_currencies:
        return []

    # Формируем строку с валютами для запроса
    currencies = ','.join(user_currencies)
    url = f"http://api.currencylayer.com/live?access_key={CURRENCY_LAYER_API_KEY}&currencies={currencies}&source=RUB"

    response = requests.get(url)
    data = response.json()

    rates = []
    if data.get('success'):
        for currency in user_currencies:
            rate_key = f"RUB{currency}"
            if rate_key in data['quotes']:
                rates.append({
                    "currency": currency,
                    "rate": round(1 / data['quotes'][rate_key], 2)  # Округляем до 2 знаков после запятой
                })

    return rates


print(get_currency_rates())


