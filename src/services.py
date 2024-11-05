import json
import logging
from src.transaction_parser import read_transactions_from_excel
import os

# Настройка логирования для services.py
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)  # Создание директории, если её нет
log_file = os.path.join(log_dir, "search_transactions.log")

logger = logging.getLogger("services")
logger.setLevel(logging.INFO)

# Создание обработчика, записывающего логи в файл
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)

def search_transactions(search_str):
    """Возвращает JSON с транзакциями, содержащими поисковую строку в категории или описании."""
    logger.info("Начат поиск транзакций по строке: '%s'", search_str)

    try:
        # Читаем транзакции из файла
        df = read_transactions_from_excel()
        logger.info("Транзакции успешно загружены из файла")

        if df.empty:
            logger.warning("Файл с транзакциями пуст")
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

        logger.info("Найдено %d транзакций, соответствующих запросу", len(transactions))
        return json.dumps({"transactions": transactions}, ensure_ascii=False, indent=4)

    except Exception as e:
        logger.error("Произошла ошибка при поиске транзакций: %s", e, exc_info=True)
        return json.dumps({"error": "Ошибка при обработке данных"})

# Пример вызова функции
# search_str = "Супермаркеты"
# print(search_transactions(search_str))
