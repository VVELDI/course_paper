import json
import os
from datetime import datetime

import pandas as pd

from src.transaction_parser import read_transactions_from_excel


def get_greeting():
    """Возвращает приветствие в зависимости от текущего времени."""
    current_time = datetime.now()
    hour = current_time.hour

    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


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

    return cards


def get_top_transactions(start_date, n=5):
    """Возвращает топ-5 транзакций по сумме платежа за период от start_date до настоящего времени."""
    transactions = read_transactions_from_excel()

    # Проверка, есть ли данные в DataFrame
    if transactions.empty:
        return {"top_transactions": []}

    # Преобразуем start_date в datetime
    start_date = pd.to_datetime(start_date, format="%d-%m-%Y")

    # Фильтруем транзакции по дате
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format="%d.%m.%Y %H:%M:%S")
    filtered_transactions = transactions[transactions['Дата операции'] >= start_date]

    # Извлекаем необходимые столбцы и фильтруем по количеству
    top_transactions = filtered_transactions.nlargest(n, 'Сумма платежа')[
        ['Дата операции', 'Сумма платежа', 'Категория', 'Описание']]

    # Формируем список для JSON-ответа
    result = []
    for index, row in top_transactions.iterrows():
        result.append({
            "date": row['Дата операции'].strftime("%d.%m.%Y"),
            "amount": row['Сумма платежа'],
            "category": row['Категория'],
            "description": row['Описание']
        })

    return result


# Пример вызова функции
# print(calculate_card_expenses("22-12-2021"))  # Указать дату в нужном формате
# print(get_top_transactions("22-12-2021"))  # Укажите дату в формате "дд-мм-гггг"
