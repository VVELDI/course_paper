import json
import pytest
from unittest.mock import patch
from src.views import create_response  # Измените импорт на правильный модуль


@pytest.fixture
def mock_data():
    return {
        "greeting": "Добрый день!",
        "cards": [{"id": 1, "expenses": 100}],
        "top_transactions": [
            {"id": 1, "amount": 500, "description": "Покупка"},
            {"id": 2, "amount": 300, "description": "Оплата"},
        ],
        "currency_rates": [
            {"currency": "USD", "rate": 74.0},
            {"currency": "EUR", "rate": 88.0},
        ],
        "stock_prices": [
            {"symbol": "AAPL", "price": 150.0},
            {"symbol": "GOOGL", "price": 2800.0},
        ],
    }


@patch("src.views.get_greeting")
@patch("src.views.calculate_card_expenses")
@patch("src.views.get_currency_rates")
@patch("src.views.get_top_transactions")
@patch("src.views.get_stock_prices")
def test_create_response(mock_get_stock_prices, mock_get_top_transactions, mock_get_currency_rates,
                         mock_calculate_card_expenses, mock_get_greeting, mock_data):
    # Настройка моков
    mock_get_greeting.return_value = mock_data["greeting"]
    mock_calculate_card_expenses.return_value = mock_data["cards"]
    mock_get_currency_rates.return_value = mock_data["currency_rates"]
    mock_get_top_transactions.return_value = mock_data["top_transactions"]
    mock_get_stock_prices.return_value = mock_data["stock_prices"]

    start_date = "22-12-2021"

    # Вызов функции
    response = create_response(start_date)

    # Преобразуем ответ обратно в словарь для проверки
    response_dict = json.loads(response)

    # Проверка содержимого ответа
    assert response_dict["greeting"] == mock_data["greeting"]
    assert response_dict["cards"] == mock_data["cards"]
    assert response_dict["top_transactions"] == mock_data["top_transactions"]
    assert response_dict["currency_rates"] == mock_data["currency_rates"]
    assert response_dict["stock_prices"] == mock_data["stock_prices"]


@patch("src.views.get_greeting")
@patch("src.views.calculate_card_expenses")
@patch("src.views.get_currency_rates", return_value=[])
@patch("src.views.get_top_transactions")
@patch("src.views.get_stock_prices")
def test_create_response_no_currency_rates(mock_get_stock_prices, mock_get_top_transactions, mock_get_currency_rates,
                                           mock_calculate_card_expenses, mock_get_greeting):
    # Настройка моков
    mock_get_greeting.return_value = "Добрый день!"
    mock_calculate_card_expenses.return_value = [{"id": 1, "expenses": 100}]
    mock_get_top_transactions.return_value = [{"id": 1, "amount": 500, "description": "Покупка"}]
    mock_get_stock_prices.return_value = [{"symbol": "AAPL", "price": 150.0}]

    start_date = "22-12-2021"

    # Вызов функции
    response = create_response(start_date)

    # Преобразуем ответ обратно в словарь для проверки
    response_dict = json.loads(response)

    # Проверка содержимого ответа
    assert response_dict["greeting"] == "Добрый день!"
    assert response_dict["cards"] == [{"id": 1, "expenses": 100}]
    assert response_dict["top_transactions"] == [{"id": 1, "amount": 500, "description": "Покупка"}]
    assert response_dict["currency_rates"] == []  # Проверяем, что курсы валют пустые
    assert response_dict["stock_prices"] == [{"symbol": "AAPL", "price": 150.0}]
