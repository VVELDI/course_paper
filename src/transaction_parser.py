import os
import json
import logging
import pandas as pd

# Настройка логирования для transaction_parser.py
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "file_operations.log")

logger = logging.getLogger("transaction_parser")
logger.setLevel(logging.INFO)

# Создание обработчика, записывающего логи в файл
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)

# Глобальные пути
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE_PATH = os.path.join(PROJECT_ROOT, '..', 'data', 'operations.xlsx')
USER_SETTINGS_PATH = os.path.join(PROJECT_ROOT, '..', 'data', 'user_settings.json')

def read_transactions_from_excel():
    """Считывает транзакции из Excel файла и возвращает их как DataFrame."""
    try:
        logger.info(f"Чтение транзакций из файла: {EXCEL_FILE_PATH}")
        df = pd.read_excel(EXCEL_FILE_PATH)
        logger.info("Транзакции успешно считаны из Excel файла.")
        return df
    except FileNotFoundError:
        logger.error(f"Файл {EXCEL_FILE_PATH} не найден.")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Произошла ошибка при чтении файла {EXCEL_FILE_PATH}: {e}")
        return pd.DataFrame()

def load_user_settings():
    """Загружает пользовательские настройки из JSON файла."""
    try:
        logger.info(f"Чтение пользовательских настроек из файла: {USER_SETTINGS_PATH}")
        with open(USER_SETTINGS_PATH, 'r', encoding='utf-8') as file:
            settings = json.load(file)
        logger.info("Пользовательские настройки успешно загружены.")
        return settings
    except FileNotFoundError:
        logger.error(f"Файл {USER_SETTINGS_PATH} не найден.")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле {USER_SETTINGS_PATH}. Проверьте формат файла.")
        return {}
    except Exception as e:
        logger.error(f"Произошла ошибка при загрузке файла {USER_SETTINGS_PATH}: {e}")
        return {}

# Проверка функции логирования
# load_user_settings()
# print("Проверка завершена, проверьте файл логов.")
