import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch

# Добавляем путь для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from src.classification import Category, Product, Sorting


class TestProductFeatures(unittest.TestCase):
    """Тесты для новых возможностей класса Product"""

    def setUp(self):
        """Подготовка тестовых данных"""
        self.product1 = Product("Телефон", "Смартфон", 10, 1000.0)
        self.product2 = Product("Планшет", "Планшет", 5, 2000.0)
        self.product3 = Product("Ноутбук", "Ноутбук", 3, 5000.0)

    def test_product_addition(self):
        """Тест сложения продуктов"""
        # 10 * 1000 + 5 * 2000 = 10000 + 10000 = 20000
        result = self.product1 + self.product2
        self.assertEqual(result, 20000.0)

        # 5 * 2000 + 3 * 5000 = 10000 + 15000 = 25000
        result = self.product2 + self.product3
        self.assertEqual(result, 25000.0)

    def test_product_addition_with_different_prices(self):
        """Тест сложения продуктов с разными ценами"""
        cheap_product = Product("Дешевый", "Товар", 100, 10.0)
        expensive_product = Product("Дорогой", "Товар", 2, 1000.0)

        # 100 * 10 + 2 * 1000 = 1000 + 2000 = 3000
        result = cheap_product + expensive_product
        self.assertEqual(result, 3000.0)

    def test_product_addition_type_error(self):
        """Тест ошибки типа при сложении"""
        with self.assertRaises(Exception):
            self.product1 + "не продукт"

    def test_product_string_representation(self):
        """Тест строкового представления продукта"""
        product = Product("Тест", "Описание", 15, 150.5)
        expected = "Тест, 150.5 руб. Остаток: 15 шт."
        self.assertEqual(str(product), expected)

    def test_product_price_validation(self):
        """Тест валидации цены продукта"""
        # Исходная цена
        self.assertEqual(self.product1.price, 1000.0)

        # Установка валидной цены
        self.product1.price = 1200.0
        self.assertEqual(self.product1.price, 1200.0)

        # Попытка установки невалидной цены (должна остаться прежняя)
        self.product1.price = -100.0
        self.assertEqual(self.product1.price, 1200.0)

        self.product1.price = 0
        self.assertEqual(self.product1.price, 1200.0)

    def test_new_product_classmethod(self):
        """Тест создания продукта через classmethod"""
        product_data = {"name": "Новый продукт", "description": "Описание нового", "price": 500.0, "quantity": 8}

        product = Product.new_product(product_data)
        self.assertEqual(product.name, "Новый продукт")
        self.assertEqual(product.description, "Описание нового")
        self.assertEqual(product.price, 500.0)
        self.assertEqual(product.quantity, 8)


class TestCategoryFeatures(unittest.TestCase):
    """Тесты для новых возможностей класса Category"""

    def setUp(self):
        """Подготовка тестовых данных"""
        self.product1 = Product("Товар1", "Описание1", 10, 100.0)
        self.product2 = Product("Товар2", "Описание2", 5, 200.0)
        self.product3 = Product("Товар3", "Описание3", 3, 300.0)

        self.category = Category("Тестовая категория", "Описание категории", [self.product1, self.product2])

    def test_category_string_representation(self):
        """Тест строкового представления категории"""
        # 10 + 5 = 15 товаров
        expected = "Тестовая категория, количество продуктов: 15 шт."
        self.assertEqual(str(self.category), expected)

    def test_category_total_quantity(self):
        """Тест подсчета общего количества товаров в категории"""
        self.assertEqual(self.category.total_quantity, 15)  # 10 + 5

        # Добавляем еще один товар
        self.category.add_product(self.product3)
        self.assertEqual(self.category.total_quantity, 18)  # 10 + 5 + 3

    def test_category_total_value(self):
        """Тест подсчета общей стоимости товаров в категории"""
        # (10*100) + (5*200) = 1000 + 1000 = 2000
        self.assertEqual(self.category.total_value, 2000.0)

        # Добавляем еще один товар
        self.category.add_product(self.product3)
        # 2000 + (3*300) = 2000 + 900 = 2900
        self.assertEqual(self.category.total_value, 2900.0)

    def test_category_products_property(self):
        """Тест свойства products (оптимизированная версия)"""
        products_list = self.category.products
        self.assertEqual(len(products_list), 2)

        # Проверяем формат строк
        self.assertIn("Товар1, 100.0 руб. Остаток: 10 шт.", products_list)
        self.assertIn("Товар2, 200.0 руб. Остаток: 5 шт.", products_list)

    def test_category_statistics(self):
        """Тест статистики категорий"""
        # Сбрасываем статистику для чистого теста
        Category.total_categories = 0
        Category.total_products = 0

        category1 = Category("Кат1", "Описание", [self.product1])
        category2 = Category("Кат2", "Описание", [self.product2, self.product3])

        self.assertEqual(Category.total_categories, 2)
        self.assertEqual(Category.total_products, 3)

    def test_get_products_objects(self):
        """Тест получения объектов продуктов"""
        products_objects = self.category.get_products_objects()
        self.assertEqual(len(products_objects), 2)
        self.assertIsInstance(products_objects[0], Product)
        self.assertIsInstance(products_objects[1], Product)

    def test_product_count_property(self):
        """Тест свойства product_count"""
        self.assertEqual(self.category.product_count, 2)

        self.category.add_product(self.product3)
        self.assertEqual(self.category.product_count, 3)


class TestSortingFeatures(unittest.TestCase):
    """Тесты для класса Sorting"""

    def setUp(self):
        """Подготовка тестовых данных"""
        self.product1 = Product("iPhone", "Смартфон", 10, 1000.0)
        self.product2 = Product("Samsung", "Смартфон", 5, 800.0)
        self.product3 = Product("MacBook", "Ноутбук", 3, 2000.0)
        self.product4 = Product("ThinkPad", "Ноутбук", 7, 1500.0)

        self.category_phones = Category("Смартфоны", "Мобильные телефоны", [self.product1, self.product2])

        self.category_laptops = Category("Ноутбуки", "Портативные компьютеры", [self.product3, self.product4])

        self.all_categories = [self.category_phones, self.category_laptops]

    @patch("builtins.input", return_value="Смартфоны")
    def test_sorting_initialization(self, mock_input):
        """Тест инициализации Sorting"""
        sorter = Sorting(self.all_categories)

        self.assertEqual(sorter.need_find, "Смартфоны")
        self.assertEqual(len(sorter.found_products), 2)
        self.assertEqual(sorter.found_products[0].name, "iPhone")
        self.assertEqual(sorter.found_products[1].name, "Samsung")

    @patch("builtins.input", return_value="Смартфоны")
    def test_sorting_iterator(self, mock_input):
        """Тест итератора Sorting"""
        sorter = Sorting(self.all_categories)

        # Тестируем итерацию
        products = list(sorter)
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0].name, "iPhone")
        self.assertEqual(products[1].name, "Samsung")

        # Тестируем повторную итерацию (должен сброситься индекс)
        sorter.__iter__()
        products_again = list(sorter)
        self.assertEqual(len(products_again), 2)

    @patch("builtins.input", return_value="Несуществующая")
    def test_sorting_category_not_found(self, mock_input):
        """Тест поиска несуществующей категории"""
        sorter = Sorting(self.all_categories)

        self.assertEqual(sorter.need_find, "Несуществующая")
        self.assertEqual(len(sorter.found_products), 0)
        self.assertEqual(sorter.found_products, [])

    @patch("builtins.input", return_value="смартфоны")  # нижний регистр
    def test_sorting_case_insensitive(self, mock_input):
        """Тест регистронезависимого поиска"""
        sorter = Sorting(self.all_categories)

        self.assertEqual(len(sorter.found_products), 2)
        self.assertEqual(sorter.found_products[0].name, "iPhone")

    @patch("builtins.input", return_value="Смартфоны")
    @patch("sys.stdout", new_callable=StringIO)
    def test_print_sorted_products_found(self, mock_stdout, mock_input):
        """Тест вывода найденных продуктов"""
        sorter = Sorting(self.all_categories)
        sorter.print_sorted_products()

        output = mock_stdout.getvalue()
        self.assertIn("ПРОДУКТЫ В КАТЕГОРИИ 'Смартфоны'", output)
        self.assertIn("iPhone", output)
        self.assertIn("Samsung", output)

    @patch("builtins.input", return_value="Несуществующая")
    @patch("sys.stdout", new_callable=StringIO)
    def test_print_sorted_products_not_found(self, mock_stdout, mock_input):
        """Тест вывода при ненайденной категории"""
        sorter = Sorting(self.all_categories)
        sorter.print_sorted_products()

        output = mock_stdout.getvalue()
        self.assertIn("Категория 'Несуществующая' не найдена или пуста", output)


class TestIntegrationFeatures(unittest.TestCase):
    """Интеграционные тесты"""

    def test_product_addition_in_category(self):
        """Тест сложения продуктов внутри категории"""
        product_a = Product("A", "Товар A", 10, 100.0)
        product_b = Product("B", "Товар B", 2, 200.0)

        category = Category("Тест", "Описание", [product_a, product_b])

        # Сложение продуктов из категории
        total_value = product_a + product_b
        self.assertEqual(total_value, 1400.0)  # 10*100 + 2*200 = 1400

        # Проверяем, что total_value категории совпадает
        self.assertEqual(category.total_value, 1400.0)

    def test_complex_scenario(self):
        """Тест сложного сценария со всеми функциями"""
        # Создаем продукты
        phone1 = Product("Phone1", "Смартфон", 5, 500.0)
        phone2 = Product("Phone2", "Смартфон", 3, 700.0)
        laptop1 = Product("Laptop1", "Ноутбук", 2, 1000.0)
        laptop2 = Product("Laptop2", "Ноутбук", 1, 1500.0)

        # Создаем категории
        phones_category = Category("Телефоны", "Мобильные", [phone1, phone2])
        laptops_category = Category("Ноутбуки", "Компьютеры", [laptop1, laptop2])

        categories = [phones_category, laptops_category]

        # Тестируем сложение
        phone_total = phone1 + phone2  # 5*500 + 3*700 = 2500 + 2100 = 4600
        laptop_total = laptop1 + laptop2  # 2*1000 + 1*1500 = 2000 + 1500 = 3500

        self.assertEqual(phone_total, 4600.0)
        self.assertEqual(laptop_total, 3500.0)

        # Тестируем строковые представления
        self.assertEqual(str(phones_category), "Телефоны, количество продуктов: 8 шт.")
        self.assertEqual(str(laptops_category), "Ноутбуки, количество продуктов: 3 шт.")


class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев"""

    def test_empty_category(self):
        """Тест пустой категории"""
        empty_category = Category("Пустая", "Описание", [])
        self.assertEqual(str(empty_category), "Пустая, количество продуктов: 0 шт.")
        self.assertEqual(empty_category.total_value, 0.0)
        self.assertEqual(empty_category.products, [])
        self.assertEqual(empty_category.get_products_objects(), [])

    def test_single_product_category(self):
        """Тест категории с одним продуктом"""
        product = Product("Один", "Товар", 1, 100.0)
        category = Category("Одна", "Описание", [product])

        self.assertEqual(str(category), "Одна, количество продуктов: 1 шт.")
        self.assertEqual(category.total_value, 100.0)

    def test_product_with_zero_quantity(self):
        """Тест продукта с нулевым количеством"""
        zero_product = Product("Ноль", "Товар", 0, 100.0)
        normal_product = Product("Норма", "Товар", 5, 50.0)

        # Сложение с нулевым количеством
        result = zero_product + normal_product  # 0*100 + 5*50 = 0 + 250 = 250
        self.assertEqual(result, 250.0)

    def test_product_with_negative_price_attempt(self):
        """Тест попытки установки отрицательной цены"""
        product = Product("Тест", "Товар", 10, 100.0)

        # Попытка установить отрицательную цену
        product.price = -50.0

        # Цена должна остаться прежней
        self.assertEqual(product.price, 100.0)


if __name__ == "__main__":
    # Запуск тестов
    unittest.main(verbosity=2)
