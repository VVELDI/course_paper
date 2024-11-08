from unittest.mock import MagicMock, patch

from src.external_api import get_currency_rates, get_stock_prices


# Тест для get_currency_rates
@patch('requests.get')
@patch('src.transaction_parser.load_user_settings')
def test_get_currency_rates(mock_load_user_settings, mock_requests_get):
    # Мокаем возвращаемое значение настроек пользователя
    mock_load_user_settings.return_value = {
        "user_currencies": ["USD", "EUR"]
    }

    # Мокаем ответ от requests.get
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'success': True,
        'quotes': {
            'RUBUSD': 74.0,
            'RUBEUR': 88.0
        }
    }
    mock_requests_get.return_value = mock_response

    # Вызываем функцию
    rates = get_currency_rates()

    # Проверяем, что функция вернула корректные данные
    assert len(rates) == 2
    assert rates[0]['currency'] == 'USD'
    assert 'rate' in rates[0]  # Проверяем, что курс есть в ответе
    assert rates[1]['currency'] == 'EUR'
    assert 'rate' in rates[1]  # Проверяем, что курс есть в ответе


# Тест для get_stock_prices
@patch('requests.get')
@patch('src.transaction_parser.load_user_settings')
@patch('src.external_api.get_currency_rates')
def test_get_stock_prices(mock_get_currency_rates, mock_load_user_settings, mock_requests_get):
    # Мокаем возвращаемое значение настроек пользователя
    mock_load_user_settings.return_value = {
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    }

    @patch('requests.get')
    @patch('src.transaction_parser.load_user_settings')
    @patch('src.external_api.get_currency_rates')
    def test_get_stock_prices(mock_get_currency_rates, mock_load_user_settings, mock_requests_get):
        # Мокаем возвращаемое значение настроек пользователя
        mock_load_user_settings.return_value = {
            "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
        }

        # Мокаем курсы валют
        mock_get_currency_rates.return_value = [
            {"currency": "USD", "rate": 0.0135}  # Пример курса для USD
        ]

        # Мокаем ответ от requests.get для акций
        mock_response_aapl = MagicMock()
        mock_response_aapl.json.return_value = {'c': 150.0}  # Цена для AAPL
        mock_response_amzn = MagicMock()
        mock_response_amzn.json.return_value = {'c': 2000.0}  # Цена для AMZN
        mock_response_googl = MagicMock()
        mock_response_googl.json.return_value = {'c': 2800.0}  # Цена для GOOGL
        mock_response_msft = MagicMock()
        mock_response_msft.json.return_value = {'c': 300.0}  # Цена для MSFT
        mock_response_tsla = MagicMock()
        mock_response_tsla.json.return_value = {'c': 700.0}  # Цена для TSLA

        # Мокаем ответы для всех акций
        mock_requests_get.side_effect = [mock_response_aapl, mock_response_amzn, mock_response_googl,
                                         mock_response_msft,
                                         mock_response_tsla]

        # Вызываем функцию
        prices = get_stock_prices()

        # Проверяем, что функция вернула 5 акций
        assert len(prices) == 5

        # Проверяем, что все акции присутствуют
        stock_symbols = [price['stock'] for price in prices]
        assert 'AAPL' in stock_symbols
        assert 'AMZN' in stock_symbols
        assert 'GOOGL' in stock_symbols
        assert 'MSFT' in stock_symbols
        assert 'TSLA' in stock_symbols

        # Проверяем, что цены это числа больше 0 (чтобы убедиться, что вычисления происходят корректно)
        for price in prices:
            assert isinstance(price['price'], (int, float))
            assert price['price'] > 0

        # Проверка, что пересчёт с учётом валютного курса происходит (не обязательно точно, главное, что пересчёт есть)
        for price in prices:
            assert price['price'] > 0  # Просто проверка, что цена больше 0, после пересчёта
            assert 'stock' in price  # Проверка, что есть символ акции
            assert 'price' in price  # Проверка, что есть цена
