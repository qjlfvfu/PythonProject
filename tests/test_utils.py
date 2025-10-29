import json
import os
import sys
import unittest
from unittest.mock import mock_open, patch

from src.utils import load_transactions

# Добавляем путь для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))


class TestLoadTransactions(unittest.TestCase):
    """Тесты для функции load_transactions"""

    def test_load_valid_json_list(self):
        """Тест загрузки валидного JSON списка"""
        test_data = [
            {"name": "Категория1", "products": [{"name": "Товар1", "price": 100}]},
            {"name": "Категория2", "products": [{"name": "Товар2", "price": 200}]},
        ]

        mock_json = json.dumps(test_data)

        with patch("builtins.open", mock_open(read_data=mock_json)):
            result = load_transactions("test.json")

        self.assertEqual(result, test_data)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

    def test_load_valid_json_dict_returns_empty_list(self):
        """Тест загрузки JSON словаря (не списка) возвращает пустой список"""
        test_data = {"name": "Категория1", "products": [{"name": "Товар1", "price": 100}]}

        mock_json = json.dumps(test_data)

        with patch("builtins.open", mock_open(read_data=mock_json)):
            result = load_transactions("test.json")

        self.assertEqual(result, [])
        self.assertIsInstance(result, list)

    def test_load_empty_list(self):
        """Тест загрузки пустого списка"""
        test_data = []

        mock_json = json.dumps(test_data)

        with patch("builtins.open", mock_open(read_data=mock_json)):
            result = load_transactions("test.json")

        self.assertEqual(result, [])
        self.assertIsInstance(result, list)

    def test_file_not_found(self):
        """Тест обработки отсутствующего файла"""
        with patch("builtins.open", side_effect=FileNotFoundError()):
            result = load_transactions("nonexistent.json")

        self.assertEqual(result, [])
        self.assertIsInstance(result, list)

    def test_invalid_json_format(self):
        """Тест обработки невалидного JSON"""
        invalid_json = "{invalid json}"

        with patch("builtins.open", mock_open(read_data=invalid_json)):
            with patch("builtins.print") as mock_print:
                result = load_transactions("invalid.json")

        self.assertEqual(result, [])
        self.assertIsInstance(result, list)
        # Проверяем что было напечатано сообщение об ошибке
        mock_print.assert_called_once()

    def test_json_decode_error_empty_file(self):
        """Тест обработки пустого файла (JSONDecodeError)"""
        with patch("builtins.open", mock_open(read_data="")):
            with patch("builtins.print") as mock_print:
                result = load_transactions("empty.json")

        self.assertEqual(result, [])
        self.assertIsInstance(result, list)
        # Проверяем что было напечатано сообщение об ошибке
        mock_print.assert_called_once()

    def test_general_exception(self):
        """Тест обработки общего исключения"""
        with patch("builtins.open", side_effect=Exception("Some error")):
            result = load_transactions("error.json")

        self.assertEqual(result, [])
        self.assertIsInstance(result, list)

    def test_encoding_issues(self):
        """Тест проблем с кодировкой"""
        test_data = [{"name": "Тест", "products": []}]
        mock_json = json.dumps(test_data, ensure_ascii=False)

        with patch("builtins.open", mock_open(read_data=mock_json.encode("utf-8"))):
            # Передаем байты чтобы проверить кодировку
            file_mock = mock_open(read_data=mock_json)
            file_mock.return_value.__enter__.return_value.read.return_value = mock_json

            result = load_transactions("unicode.json")

        self.assertEqual(result, test_data)

    def test_complex_data_structure(self):
        """Тест загрузки сложной структуры данных"""
        test_data = [
            {
                "name": "Электроника",
                "description": "Технические устройства",
                "products": [
                    {"name": "Смартфон", "description": "Мобильный телефон", "price": 500.0, "quantity": 10},
                    {"name": "Ноутбук", "description": "Портативный компьютер", "price": 1000.0, "quantity": 5},
                ],
            },
            {
                "name": "Книги",
                "description": "Печатные издания",
                "products": [
                    {"name": "Роман", "description": "Художественная литература", "price": 20.0, "quantity": 50}
                ],
            },
        ]

        mock_json = json.dumps(test_data, ensure_ascii=False)

        with patch("builtins.open", mock_open(read_data=mock_json)):
            result = load_transactions("complex.json")

        self.assertEqual(result, test_data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Электроника")
        self.assertEqual(len(result[0]["products"]), 2)
        self.assertEqual(result[1]["name"], "Книги")

    def test_file_path_usage(self):
        """Тест что правильный путь к файлу используется"""
        test_data = [{"test": "data"}]
        mock_json = json.dumps(test_data)

        with patch("builtins.open", mock_open(read_data=mock_json)) as mock_file:
            result = load_transactions("specific_path.json")

            # Проверяем что open был вызван с правильным путем
            mock_file.assert_called_once_with("specific_path.json", "r", encoding="utf-8")

    def test_nested_exception_handling(self):
        """Тест вложенных исключений"""
        # Сначала FileNotFoundError, потом общее исключение
        with patch("builtins.open", side_effect=FileNotFoundError()):
            result1 = load_transactions("nonexistent.json")
            self.assertEqual(result1, [])

        with patch("builtins.open", side_effect=Exception("Unexpected")):
            result2 = load_transactions("error.json")
            self.assertEqual(result2, [])


class TestLoadTransactionsIntegration(unittest.TestCase):
    """Интеграционные тесты для load_transactions"""

    def test_with_real_file_creation(self):
        """Тест с созданием реального временного файла"""
        import tempfile

        test_data = [{"name": "Временная категория", "products": [{"name": "Временный товар", "price": 100}]}]

        # Создаем временный файл с явным указанием кодировки и режима
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", encoding="utf-8", delete=False) as temp_file:
            json.dump(test_data, temp_file, ensure_ascii=False)
            temp_path = temp_file.name

        try:
            # Закрываем файл перед чтением
            # Загружаем данные из временного файла
            result = load_transactions(temp_path)

            self.assertEqual(result, test_data)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["name"], "Временная категория")

        finally:
            # Удаляем временный файл
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_with_real_file_creation_alternative(self):
        """Альтернативный тест с реальным файлом"""
        import tempfile

        test_data = [{"name": "Тест категория", "products": [{"name": "Тест товар", "price": 50}]}]

        # Создаем файл вручную
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, "test_transactions.json")

        try:
            # Записываем данные в файл
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(test_data, f, ensure_ascii=False)

            # Читаем через нашу функцию
            result = load_transactions(temp_path)

            self.assertEqual(result, test_data)
            self.assertEqual(len(result), 1)

        finally:
            # Удаляем файл
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_empty_json_file(self):
        """Тест с пустым JSON файлом"""
        import tempfile

        # Создаем пустой файл
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, "empty_test.json")

        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write("")

            with patch("builtins.print") as mock_print:
                result = load_transactions(temp_path)

            self.assertEqual(result, [])
            # Проверяем что было напечатано сообщение об ошибке
            mock_print.assert_called_once()

        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_malformed_json_file(self):
        """Тест с поврежденным JSON файлом"""
        import tempfile

        # Создаем файл с невалидным JSON
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, "malformed_test.json")

        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write("{invalid json")

            with patch("builtins.print") as mock_print:
                result = load_transactions(temp_path)

            self.assertEqual(result, [])
            # Проверяем что было напечатано сообщение об ошибке
            mock_print.assert_called_once()

        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_file_not_found_integration(self):
        """Тест отсутствующего файла в интеграционном режиме"""
        import tempfile

        # Создаем путь к несуществующему файлу
        temp_dir = tempfile.gettempdir()
        nonexistent_path = os.path.join(temp_dir, "nonexistent_file_12345.json")

        # Убеждаемся что файла нет
        if os.path.exists(nonexistent_path):
            os.unlink(nonexistent_path)

        result = load_transactions(nonexistent_path)
        self.assertEqual(result, [])


class TestLoadTransactionsEdgeCases(unittest.TestCase):
    """Тесты граничных случаев"""

    def test_very_large_json(self):
        """Тест очень большого JSON файла"""
        large_data = [{"id": i, "data": "x" * 100} for i in range(100)]

        with patch("builtins.open", mock_open(read_data=json.dumps(large_data))):
            result = load_transactions("large.json")

        self.assertEqual(len(result), 100)
        self.assertEqual(result[0]["id"], 0)
        self.assertEqual(result[-1]["id"], 99)

    def test_unicode_characters(self):
        """Тест Unicode символов"""
        test_data = [
            {"name": "Товар с русскими буквами", "description": "Описание с émojis 🚀"},
            {"name": "商品", "description": "中文描述"},
        ]

        with patch("builtins.open", mock_open(read_data=json.dumps(test_data, ensure_ascii=False))):
            result = load_transactions("unicode.json")

        self.assertEqual(result, test_data)
        self.assertEqual(result[0]["name"], "Товар с русскими буквами")
        self.assertEqual(result[1]["name"], "商品")

    def test_special_json_values(self):
        """Тест специальных JSON значений"""
        test_data = [{"null_value": None, "bool_value": True, "number": 123.45, "nested": {"key": "value"}}]

        with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
            result = load_transactions("special_values.json")

        self.assertEqual(result, test_data)
        self.assertIsNone(result[0]["null_value"])
        self.assertTrue(result[0]["bool_value"])
        self.assertEqual(result[0]["number"], 123.45)

    def test_permission_error_handling(self):
        """Тест обработки ошибок прав доступа"""
        with patch("builtins.open", side_effect=PermissionError("Permission denied")):
            result = load_transactions("/root/protected.json")
            self.assertEqual(result, [])


if __name__ == "__main__":
    # Запуск тестов с покрытием
    import pytest

    print("=== ТЕСТИРОВАНИЕ UTILS ===")
    pytest.main([__file__, "-v", "--cov=src.utils", "--cov-report=term-missing", "--cov-report=html"])
