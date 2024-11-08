from datetime import datetime
from unittest.mock import patch

import pytest

from src.reports import spending_by_weekday


@pytest.fixture
def sample_transactions():
    import pandas as pd
    data = {
        "Дата операции": ["2021-01-10", "2021-01-11", "2021-01-12", None, None, "2022-01-01"],
        "Сумма операции": [100, 200, 150, 50, 300, 400]
    }
    df = pd.DataFrame(data)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"])
    return df


def test_spending_by_weekday(sample_transactions):
    test_date = "2021-01-10"  # Тестируем на дату, за которую есть транзакции

    with patch("src.reports.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime.strptime(test_date, "%Y-%m-%d")

        # Запускаем функцию и получаем результат
        result = spending_by_weekday(sample_transactions, date=test_date)

        # Проверяем, что результат — это словарь с данными по дням недели
        assert isinstance(result, dict)

        # Проверяем, что хотя бы один день недели присутствует в ответе
        assert any(day in result for day in
                   ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"])


def test_logging(sample_transactions):
    with patch("src.reports.logger") as mock_logger:
        # Запускаем функцию для получения отчета
        spending_by_weekday(sample_transactions, date="2021-01-10")

        # Проверяем, что логируется информация
        mock_logger.info.assert_called()

        # Проверяем, что предупреждение не было вызвано (если данные есть)
        mock_logger.warning.assert_not_called()
