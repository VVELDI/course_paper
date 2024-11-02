from datetime import datetime

import pandas as pd

from src.transaction_parser import read_transactions_from_excel


def calculate_card_expenses(start_date):
    """Расчет расходов по картам за указанный период."""
    transactions = read_transactions_from_excel()

    # Преобразуем дату в формат datetime
    start_date = pd.to_datetime(start_date, dayfirst=True)  # Указываем, что день идет первым
    current_date = datetime.now()

    # Словарь для хранения данных по картам
    card_data = {}

    for index, row in transactions.iterrows():
        transaction_date = pd.to_datetime(row['Дата операции'], dayfirst=True)  # Указываем формат
        card_number = row['Номер карты']

        # Проверка на наличие номера карты
        if pd.isna(card_number):
            continue  # Пропускаем строки без номера карты

        amount = row['Сумма операции']
        last_digits = str(card_number)[-4:]  # Приводим к строке для получения последних 4 цифр

        # Инициализируем данные для карты, если их еще нет
        if last_digits not in card_data:
            card_data[last_digits] = {
                "total_spent": 0,
                "cashback": 0
            }

        # Если дата транзакции в пределах заданного диапазона, обновляем общую сумму и кешбэк
        if transaction_date >= start_date and transaction_date <= current_date:
            card_data[last_digits]["total_spent"] += amount
            card_data[last_digits]["cashback"] += amount / 100  # 1 рубль за каждые 100 рублей

    # Формируем список для JSON-ответа
    cards = [
        {
            "last_digits": digits,
            "total_spent": data["total_spent"],
            "cashback": data["cashback"]
        }
        for digits, data in card_data.items()
    ]

    return {
        "cards": cards
    }


# Пример вызова функции
print(calculate_card_expenses("22-12-2021"))  # Указать дату в нужном формате
