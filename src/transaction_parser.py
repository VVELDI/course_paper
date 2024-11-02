import pandas as pd
import os


# Глобальная переменная для хранения пути к файлу
# Глобальная переменная для хранения пути к корню проекта
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Путь к файлу operations.xlsx
EXCEL_FILE_PATH = os.path.join(PROJECT_ROOT, '..', 'data', 'operations.xlsx')
print(EXCEL_FILE_PATH)
def read_transactions_from_excel():
    """Считывает транзакции из Excel файла и возвращает их как DataFrame."""
    try:
        df = pd.read_excel(EXCEL_FILE_PATH)
        return df
    except FileNotFoundError:
        print(f"Файл {EXCEL_FILE_PATH} не найден.")
        return pd.DataFrame()  # Возвращаем пустой DataFrame в случае ошибки
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return pd.DataFrame()  # Возвращаем пустой DataFrame в случае ошибки

