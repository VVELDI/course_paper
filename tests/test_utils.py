import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import pandas as pd
from src.utils import get_greeting, calculate_card_expenses, get_top_transactions

# Тест для функции get_greeting
@patch("src.utils.datetime")
def test_get_greeting(mock_datetime):
    # Устанавливаем текущее время для каждого периода
    mock_datetime.now.return_value = datetime(2023, 1, 1, 6)  # Утро
    assert get_greeting() == "Доброе утро"

    mock_datetime.now.return_value = datetime(2023, 1, 1, 13)  # День
    assert get_greeting() == "Добрый день"

    mock_datetime.now.return_value = datetime(2023, 1, 1, 19)  # Вечер
    assert get_greeting() == "Добрый вечер"

    mock_datetime.now.return_value = datetime(2023, 1, 1, 1)  # Ночь
    assert get_greeting() == "Доброй ночи"

# Тест для функции calculate_card_expenses
@patch("src.utils.read_transactions_from_excel")
def test_calculate_card_expenses(mock_read_transactions):
    # Создаем фиктивные данные транзакций
    mock_data = pd.DataFrame({
        "Дата операции": ["01.01.2022", "15.01.2022", "30.01.2022"],
        "Номер карты": ["1234567890123456", "1234567890123456", "9876543210987654"],
        "Сумма операции": [1000, 1500, 2000]
    })
    mock_read_transactions.return_value = mock_data

    # Запускаем тестовую функцию с датой начала
    start_date = "01-01-2022"
    expenses = calculate_card_expenses(start_date)

    assert len(expenses) == 2
    assert expenses[0]["last_digits"] == "3456"
    assert expenses[0]["total_spent"] == 2500
    assert expenses[0]["cashback"] == 25.0
    assert expenses[1]["last_digits"] == "7654"
    assert expenses[1]["total_spent"] == 2000
    assert expenses[1]["cashback"] == 20.0

# Тест для функции get_top_transactions
@patch("src.utils.read_transactions_from_excel")
def test_get_top_transactions(mock_read_transactions):
    # Создаем фиктивные данные транзакций
    mock_data = pd.DataFrame({
        "Дата операции": ["01.01.2022 10:00:00", "05.01.2022 12:30:00", "10.01.2022 09:45:00"],
        "Сумма платежа": [100, 200, 300],
        "Категория": ["Продукты", "Развлечения", "Транспорт"],
        "Описание": ["Покупка еды", "Билеты в кино", "Поездка на метро"]
    })
    mock_read_transactions.return_value = mock_data

    # Запускаем тестовую функцию с датой начала
    start_date = "01-01-2022"
    top_transactions = get_top_transactions(start_date)

    assert len(top_transactions) == 3
    assert top_transactions[0]["amount"] == 300
    assert top_transactions[0]["category"] == "Транспорт"
    assert top_transactions[1]["amount"] == 200
    assert top_transactions[1]["category"] == "Развлечения"
    assert top_transactions[2]["amount"] == 100
    assert top_transactions[2]["category"] == "Продукты"

# Тест для обработки пустых транзакций
@patch("src.utils.read_transactions_from_excel")
def test_calculate_card_expenses_empty(mock_read_transactions):
    mock_read_transactions.return_value = pd.DataFrame(columns=["Дата операции", "Номер карты", "Сумма операции"])
    start_date = "01-01-2022"
    assert calculate_card_expenses(start_date) == []

@patch("src.utils.read_transactions_from_excel")
def test_get_top_transactions_empty(mock_read_transactions):
    mock_read_transactions.return_value = pd.DataFrame(columns=["Дата операции", "Сумма платежа", "Категория", "Описание"])
    start_date = "01-01-2022"
    result = get_top_transactions(start_date)
    assert result["top_transactions"] == []
