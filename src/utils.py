import json
import os
from datetime import datetime
import logging
import pandas as pd

from src.transaction_parser import read_transactions_from_excel

# Путь к файлу логов
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
log_file = os.path.join(log_dir, 'app.log')

# Проверка и создание папки logs, если она отсутствует
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Настройка логирования
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode='w',
    encoding='utf-8'  # Задаем кодировку UTF-8
)
logger = logging.getLogger(__name__)


def get_greeting():
    """Возвращает приветствие в зависимости от текущего времени."""
    try:
        current_time = datetime.now()
        hour = current_time.hour
        logger.debug(f"Current hour: {hour}")

        if 5 <= hour < 12:
            greeting = "Доброе утро"
        elif 12 <= hour < 18:
            greeting = "Добрый день"
        elif 18 <= hour < 23:
            greeting = "Добрый вечер"
        else:
            greeting = "Доброй ночи"

        logger.info(f"Greeting generated: {greeting}")
        return greeting
    except Exception as e:
        logger.error(f"Error in get_greeting: {e}")
        return "Привет"


def calculate_card_expenses(start_date):
    """Расчет расходов по картам за указанный период."""
    logger.info(f"Starting calculation of card expenses from {start_date}")
    try:
        transactions = read_transactions_from_excel()
        start_date = pd.to_datetime(start_date, dayfirst=True)
        current_date = datetime.now()

        card_data = {}
        for index, row in transactions.iterrows():
            transaction_date = pd.to_datetime(row['Дата операции'], dayfirst=True)
            card_number = row['Номер карты']

            if pd.isna(card_number):
                logger.debug(f"Skipping transaction without card number at index {index}")
                continue

            amount = row['Сумма операции']
            last_digits = str(card_number)[-4:]

            if last_digits not in card_data:
                card_data[last_digits] = {"total_spent": 0, "cashback": 0}

            if start_date <= transaction_date <= current_date:
                card_data[last_digits]["total_spent"] += amount
                card_data[last_digits]["cashback"] += amount / 100

        logger.info("Card expenses calculated successfully.")
        return [
            {"last_digits": digits, "total_spent": data["total_spent"], "cashback": data["cashback"]}
            for digits, data in card_data.items()
        ]
    except Exception as e:
        logger.error(f"Error in calculate_card_expenses: {e}")
        return []


def get_top_transactions(start_date, n=5):
    """Возвращает топ-5 транзакций по сумме платежа за период от start_date до настоящего времени."""
    logger.info(f"Fetching top {n} transactions from {start_date}")
    try:
        transactions = read_transactions_from_excel()

        if transactions.empty:
            logger.warning("No transactions available.")
            return {"top_transactions": []}

        start_date = pd.to_datetime(start_date, format="%d-%m-%Y")
        transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format="%d.%m.%Y %H:%M:%S")
        filtered_transactions = transactions[transactions['Дата операции'] >= start_date]

        top_transactions = filtered_transactions.nlargest(n, 'Сумма платежа')[
            ['Дата операции', 'Сумма платежа', 'Категория', 'Описание']]

        logger.info(f"Top {n} transactions fetched successfully.")
        return [
            {
                "date": row['Дата операции'].strftime("%d.%m.%Y"),
                "amount": row['Сумма платежа'],
                "category": row['Категория'],
                "description": row['Описание']
            }
            for index, row in top_transactions.iterrows()
        ]
    except Exception as e:
        logger.error(f"Error in get_top_transactions: {e}")
        return {"top_transactions": []}

# Пример вызова функции
# print(calculate_card_expenses("22-12-2021"))  # Указать дату в нужном формате
# print(get_top_transactions("22-12-2021"))  # Укажите дату в формате "дд-мм-гггг"
