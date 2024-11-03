import json

from src.transaction_parser import read_transactions_from_excel


def search_transactions(search_str):
    """Возвращает JSON с транзакциями, содержащими поисковую строку в категории или описании."""
    # Читаем транзакции из файла
    df = read_transactions_from_excel()

    if df.empty:
        return json.dumps({"error": "Нет данных для поиска"})

    # Приводим нужные столбцы к строкам для возможности поиска
    df["Категория"] = df["Категория"].astype(str)
    df["Описание"] = df["Описание"].astype(str)

    # Фильтруем транзакции по совпадению строки в категории или описании
    mask = df["Категория"].str.contains(search_str, case=False, na=False) | \
           df["Описание"].str.contains(search_str, case=False, na=False)
    result_df = df[mask]

    # Преобразуем результат в список словарей и затем в JSON
    transactions = result_df[[
        "Дата операции", "Номер карты", "Статус", "Сумма операции",
        "Валюта операции", "Категория", "Описание"
    ]].to_dict(orient="records")

    return json.dumps({"transactions": transactions}, ensure_ascii=False, indent=4)


# # Пример вызова функции
# search_str = "Супермаркеты"
# print(search_transactions(search_str))
