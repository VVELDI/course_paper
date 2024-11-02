import os

import requests
from dotenv import load_dotenv

from src.transaction_parser import load_user_settings

# Загружаем переменные окружения из .env файла
load_dotenv()
CURRENCY_LAYER_API_KEY = os.getenv('CURRENCY_LAYER_API_KEY')
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')


def get_currency_rates():
    settings = load_user_settings()
    user_currencies = settings.get("user_currencies", [])

    # Устанавливаем доллар по умолчанию, если он отсутствует
    if "USD" not in user_currencies:
        user_currencies.append("USD")

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


def get_stock_prices():
    settings = load_user_settings()  # Загружаем настройки пользователя
    user_stocks = settings.get("user_stocks", [])  # Получаем список акций

    if not user_stocks:
        print("Нет акций для запроса.")
        return []  # Если нет акций, возвращаем пустой список

    prices = []

    # Получаем курсы валют
    currency_rates = get_currency_rates()
    rub_to_usd = next((currency_.get('rate') for currency_ in currency_rates if currency_.get('currency') == 'USD'),
                      None)

    if rub_to_usd is None:
        print("Не удалось получить курс USD к RUB.")
        return []  # Если курс не получен, возвращаем пустой список

    # Запрашиваем цену для каждой акции по отдельности
    for stock in user_stocks:
        # Формируем URL для запроса цены акций
        url = f'https://finnhub.io/api/v1/quote?symbol={stock}&token={FINNHUB_API_KEY}'
        response = requests.get(url)
        data = response.json()

        if 'c' in data:  # Проверяем, что есть текущая цена
            last_price = data['c']  # Текущая цена

            # Переводим цену в рубли
            price_in_rub = round(last_price * rub_to_usd, 2)

            prices.append({
                "stock": stock,
                "price": price_in_rub  # Получаем текущую цену в рублях
            })
        else:
            print(f"Нет данных о ценах для {stock} в ответе API.")

    return prices
