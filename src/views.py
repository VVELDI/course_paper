from src.utils import get_greeting, calculate_card_expenses, get_top_transactions
from src.external_api import get_currency_rates


def create_response(start_date):
    greeting = get_greeting()

    # Получаем данные
    card_expenses = calculate_card_expenses(start_date)  # ваши карты с расходами
    top_transactions = get_top_transactions(start_date)  # ваши топ-5 транзакций
    currency_rates = get_currency_rates()

    # Формируем ответ без дублирования ключа
    response = {
        "greeting": greeting,
        "cards": card_expenses,  # Здесь cards - это список словарей с картами
        "top_transactions": top_transactions,  # Топ-5 транзакций
        "currency_rates": currency_rates
    }

    return response


# Пример вызова функции
start_date = "22-12-2021"  # укажите нужную дату
print(create_response(start_date))

