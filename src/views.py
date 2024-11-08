import json

from src.external_api import get_currency_rates, get_stock_prices
from src.utils import calculate_card_expenses, get_greeting, get_top_transactions


def create_response(start_date):
    greeting = get_greeting()
    # Получаем данные
    card_expenses = calculate_card_expenses(start_date)  # карты с расходами
    currency_rates = get_currency_rates()
    top_transactions = get_top_transactions(start_date)  # топ-5 транзакций

    if not currency_rates:
        print("Не удалось получить курсы валют.")
        currency_rates = []  # Установим пустой список, чтобы избежать ошибок ниже

    stock_prices = get_stock_prices()

    # Формируем ответ без дублирования ключа
    response = {
        "greeting": greeting,
        "cards": card_expenses,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
    json_response = json.dumps(response, ensure_ascii=False, indent=4)
    return json_response


# Пример вызова функции
# start_date = "22-12-2021"  # укажите нужную дату
# print(create_response(start_date))
