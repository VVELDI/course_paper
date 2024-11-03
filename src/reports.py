import json
import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional
import pandas as pd
from src.transaction_parser import read_transactions_from_excel

# Директория для сохранения отчетов
REPORTS_DIR = "reports"

# Создаем директорию, если она не существует
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

def save_report_to_file(filename=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Выполняем основную функцию и получаем результат
            result = func(*args, **kwargs)

            # Генерируем имя файла, если оно не передано
            if filename is None:
                generated_filename = f"report_{func.__name__}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
            else:
                generated_filename = filename

            # Полный путь к файлу
            file_path = os.path.join(REPORTS_DIR, generated_filename)

            # Сохраняем результат в JSON-файл
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)

            print(f"Отчет сохранен в файл: {file_path}")
            return result

        return wrapper

    if callable(filename):
        func = filename
        filename = None
        return decorator(func)
    else:
        return decorator


# Функция для расчета средних трат по дням недели за последние 3 месяца
@save_report_to_file
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> dict:
    # Устанавливаем дату отчёта
    report_date = pd.to_datetime(date) if date else datetime.now()

    # Определяем дату начала отчёта (три месяца назад)
    start_date = report_date - timedelta(days=90)

    # Преобразуем столбец с датой операции в формат datetime
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], errors="coerce", dayfirst=True)

    # Фильтруем данные за последние три месяца
    filtered_transactions = transactions[
        (transactions["Дата операции"] >= start_date) &
        (transactions["Дата операции"] <= report_date)
    ]

    # Если данных нет, возвращаем пустой результат
    if filtered_transactions.empty:
        return {}

    # Вычисляем траты по дням недели
    filtered_transactions = filtered_transactions.assign(weekday=filtered_transactions["Дата операции"].dt.day_name())
    weekday_expenses = filtered_transactions.groupby("weekday")["Сумма операции"].mean().round(2)

    # Приводим к формату словаря и заменяем названия дней недели на русские
    report_data = weekday_expenses.to_dict()
    report_data_ru = {
        'Понедельник': report_data.get('Monday', 0),
        'Вторник': report_data.get('Tuesday', 0),
        'Среда': report_data.get('Wednesday', 0),
        'Четверг': report_data.get('Thursday', 0),
        'Пятница': report_data.get('Friday', 0),
        'Суббота': report_data.get('Saturday', 0),
        'Воскресенье': report_data.get('Sunday', 0)
    }

    return report_data_ru
# Пример загрузки данных
# transactions = read_transactions_from_excel()
# print("Загруженные данные транзакций:", transactions.head())  # Отображаем первые строки для проверки
#
# # Запускаем функцию с сохранением результата в файл
# result = spending_by_weekday(transactions, date="2021-12-31")

