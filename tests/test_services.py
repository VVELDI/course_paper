import json
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.services import search_transactions


# Фикстура для создания поддельных данных транзакций
@pytest.fixture
def sample_transactions():
    return [
        {
            "Дата операции": "2024-10-01",
            "Номер карты": "**** 1234",
            "Статус": "Завершено",
            "Сумма операции": 100.0,
            "Валюта операции": "RUB",
            "Категория": "Супермаркеты",
            "Описание": "Покупка в супермаркете"
        },
        {
            "Дата операции": "2024-10-02",
            "Номер карты": "**** 5678",
            "Статус": "Ожидает",
            "Сумма операции": 50.0,
            "Валюта операции": "RUB",
            "Категория": "Кафе",
            "Описание": "Кофе на вынос"
        }
    ]


# Тест с параметризацией: проверка поиска по разным строкам
@pytest.mark.parametrize("search_str,expected_count", [
    ("супермаркет", 1),  # Один результат
    ("Кафе", 1),  # Один результат
    ("Отдых", 0),  # Нет совпадений
])
@patch("src.services.read_transactions_from_excel")
def test_search_transactions(mock_read_transactions, search_str, expected_count, sample_transactions):
    # Подменяем возвращаемое значение функции read_transactions_from_excel
    mock_df = MagicMock()
    mock_df.to_dict.return_value = sample_transactions
    mock_read_transactions.return_value = mock_df

    # Преобразуем sample_transactions в DataFrame для корректного теста
    mock_df = pd.DataFrame(sample_transactions)
    mock_read_transactions.return_value = mock_df

    # Вызываем тестируемую функцию
    result_json = search_transactions(search_str)
    result = json.loads(result_json)

    # Проверяем содержимое результата
    if expected_count > 0:
        assert "transactions" in result
        assert len(result["transactions"]) == expected_count
    else:
        # Проверяем, что не найдено транзакций, и возвращается пустой список
        assert "transactions" in result
        assert len(result["transactions"]) == 0  # Убедитесь, что список пустой


# Тест на случай пустого файла
@patch("src.services.read_transactions_from_excel")
def test_search_transactions_empty_file(mock_read_transactions):
    # Мокаем пустой DataFrame
    mock_read_transactions.return_value = pd.DataFrame()

    # Проверяем результат функции
    result_json = search_transactions("Супермаркет")
    result = json.loads(result_json)

    assert "error" in result
    assert result["error"] == "Нет данных для поиска"


# Тест на случай ошибки
@patch("src.services.read_transactions_from_excel")
def test_search_transactions_exception(mock_read_transactions):
    # Настраиваем mock так, чтобы он вызывал ошибку
    mock_read_transactions.side_effect = Exception("Ошибка при чтении файла")

    # Проверяем результат функции
    result_json = search_transactions("Супермаркет")
    result = json.loads(result_json)

    assert "error" in result
    assert result["error"] == "Ошибка при обработке данных"
