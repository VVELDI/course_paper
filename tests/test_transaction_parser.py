import json
from unittest.mock import patch, mock_open

import pandas as pd
import pytest

from src.transaction_parser import read_transactions_from_excel, load_user_settings


# Фикстура для создания временных данных
@pytest.fixture
def mock_excel_data():
    data = {
        "Дата операции": ["2023-01-01", "2023-01-02"],
        "Номер карты": ["1234", "5678"],
        "Сумма операции": [100.0, 200.0],
        "Категория": ["Еда", "Развлечения"],
        "Описание": ["Супермаркет", "Кинотеатр"]
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_user_settings():
    return {
        "base_currency": "RUB",
        "notifications": {"email": True, "sms": False}
    }


# Тест read_transactions_from_excel
@patch("src.transaction_parser.pd.read_excel")
def test_read_transactions_from_excel_success(mock_read_excel, mock_excel_data):
    mock_read_excel.return_value = mock_excel_data
    df = read_transactions_from_excel()
    assert not df.empty
    assert len(df) == 2
    assert df["Категория"].iloc[0] == "Еда"


@patch("src.transaction_parser.pd.read_excel")
def test_read_transactions_from_excel_file_not_found(mock_read_excel):
    mock_read_excel.side_effect = FileNotFoundError
    df = read_transactions_from_excel()
    assert df.empty


@patch("src.transaction_parser.pd.read_excel")
def test_read_transactions_from_excel_other_exception(mock_read_excel):
    mock_read_excel.side_effect = Exception("Some error")
    df = read_transactions_from_excel()
    assert df.empty


# Тест load_user_settings
@patch("builtins.open", new_callable=mock_open,
       read_data='{"base_currency": "RUB", "notifications": {"email": true, "sms": false}}')
def test_load_user_settings_success(mock_file, mock_user_settings):
    with patch("json.load", return_value=mock_user_settings):
        settings = load_user_settings()
        assert settings["base_currency"] == "RUB"
        assert settings["notifications"]["email"] is True


@patch("builtins.open", side_effect=FileNotFoundError)
def test_load_user_settings_file_not_found(mock_file):
    settings = load_user_settings()
    assert settings == {}


@patch("builtins.open", new_callable=mock_open, read_data="Invalid JSON")
def test_load_user_settings_json_decode_error(mock_file):
    with patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "", 0)):
        settings = load_user_settings()
        assert settings == {}


@patch("builtins.open", new_callable=mock_open)
def test_load_user_settings_other_exception(mock_file):
    with patch("json.load", side_effect=Exception("Some error")):
        settings = load_user_settings()
        assert settings == {}
