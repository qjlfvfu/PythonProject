import json
from typing import Dict, List


def load_transactions(file_path: str) -> List[Dict]:
    """
    Загружает данные из JSON-файла.

    Args:
        file_path (str): Путь до JSON-файла

    Returns:
        List[Dict]: Список словарей с данными транзакций или пустой список
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                return []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Файл {file_path} содержит невалидный JSON или пуст")
        return []
    except Exception:
        return []
