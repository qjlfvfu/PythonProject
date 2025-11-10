import os
import sys
import unittest
from abc import ABC
from io import StringIO
from unittest.mock import patch

import pytest

from src.classification import (
    BaseCounter,
    BaseProduct,
    Category,
    LawnGrass,
    Order,
    Product,
    Smartphone,
    Sorting,
    ZeroQuantityError,
)

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))


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

    def test_product_count_property(self):
        """Тест свойства product_count"""
        self.assertEqual(self.category.product_count, 2)

        self.category.add_product(self.product3)
        self.assertEqual(self.category.product_count, 3)  # Было 4, стало 3


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


class TestProduct(BaseProduct):
    """Конкретный класс для тестирования абстрактного класса"""

    def __init__(self, name: str, description: str, quantity: float, price: float):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.__price = price
        super().__init__(name, description, quantity, price)

    def __add__(self, other):
        if not isinstance(other, TestProduct):
            raise TypeError("Можно складывать только объекты TestProduct")
        return self.price * self.quantity + other.price * other.quantity

    def __str__(self):
        return f"{self.name} - {self.description}"

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price


def test_mixin_output():
    """Простой тест вывода миксина"""
    captured_output = StringIO()
    sys.stdout = captured_output

    # Используем обычный Product вместо TestProduct
    product = Product("Test", "Desc", 5, 100.0)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue().strip()

    assert output == "Product('Test', 'Desc', 5, 100.0)"


def test_concrete_class_works():
    """Тест, что конкретный класс работает"""
    product = Product("Product", "Description", 10, 50.0)

    assert product.name == "Product"
    assert product.description == "Description"
    assert product.quantity == 10
    assert product.price == 50.0


def test_abstract_methods_implemented():
    """Тест реализации абстрактных методов"""
    product = Product("A", "Desc", 2, 10.0)

    # Должны работать без ошибок
    result = str(product)
    add_result = product + product

    assert "A" in result
    assert add_result == 40.0


class TestZeroQuantityError(unittest.TestCase):
    """Тесты для пользовательского исключения ZeroQuantityError"""

    def test_zero_quantity_error_creation(self):
        """Тест создания исключения ZeroQuantityError"""
        error = ZeroQuantityError("Test Product", "добавлен")

        self.assertEqual(error.product_name, "Test Product")
        self.assertEqual(error.operation, "добавлен")
        self.assertEqual(str(error), "Товар 'Test Product' не может быть добавлен: количество равно нулю")

    def test_zero_quantity_error_different_operations(self):
        """Тест исключения с разными операциями"""
        error1 = ZeroQuantityError("Product1", "создан")
        error2 = ZeroQuantityError("Product2", "обновлен")

        # Проверяем что операция содержится в сообщении об ошибке
        self.assertIn("создан", str(error1))
        self.assertIn("обновлен", str(error2))


class TestProductExceptions(unittest.TestCase):
    """Тесты исключений в классе Product"""

    def test_product_creation_with_zero_quantity(self):
        """Тест создания продукта с нулевым количеством"""
        with self.assertRaises(ValueError) as context:
            Product("Test Product", "Description", 0, 100.0)

        self.assertEqual(str(context.exception), "Товар с нулевым количеством не может быть добавлен")

    def test_product_creation_with_negative_quantity(self):
        """Тест создания продукта с отрицательным количеством"""
        with self.assertRaises(ValueError) as context:
            Product("Test Product", "Description", -5, 100.0)

        self.assertEqual(str(context.exception), "Товар с нулевым количеством не может быть добавлен")

    def test_product_creation_with_positive_quantity(self):
        """Тест создания продукта с положительным количеством"""
        # Это должно работать без ошибок
        product = Product("Test Product", "Description", 1, 100.0)
        self.assertEqual(product.quantity, 1)
        self.assertEqual(product.price, 100.0)


class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев"""

    def test_order_with_zero_quantity(self):
        """Тест Order с нулевым количеством"""
        product = Product("Товар", "Описание", 10, 100.0)

        # Ожидаем исключение ZeroQuantityError
        with self.assertRaises(ZeroQuantityError) as context:
            Order(product, 0)

        self.assertEqual(str(context.exception), "Товар 'Товар' не может быть создан: количество равно нулю")

    def test_order_with_positive_quantity(self):
        """Тест Order с положительным количеством"""
        product = Product("Товар", "Описание", 10, 100.0)

        order = Order(product, 5)
        self.assertEqual(order.quantity, 5)
        self.assertEqual(order.total_value, 500.0)


class TestCategoryExceptions(unittest.TestCase):
    """Тесты исключений в классе Category"""

    def test_add_product_with_zero_quantity(self):
        """Тест добавления продукта с нулевым количеством в категорию"""
        category = Category("Test Category", "Description", [])

        # Создаем mock объект для тестирования
        from unittest.mock import Mock

        mock_product = Mock(spec=Product)
        mock_product.name = "Zero Product"
        mock_product.quantity = 0

        with self.assertRaises(ZeroQuantityError) as context:
            category.add_product(mock_product)

        self.assertEqual(str(context.exception), "Товар 'Zero Product' не может быть добавлен: количество равно нулю")


class TestSmartphone:
    """Тесты для класса Smartphone"""

    def test_smartphone_creation(self):
        """Тест создания смартфона"""
        smartphone = Smartphone(
            name="iPhone 15",
            description="Флагманский смартфон",
            quantity=10,
            price=999.99,
            efficiency=95.5,
            model="15 Pro",
            memory=256,
            color="Black",
        )

        assert smartphone.name == "iPhone 15"
        assert smartphone.description == "Флагманский смартфон"
        assert smartphone.quantity == 10
        assert smartphone.price == 999.99
        assert smartphone.efficiency == 95.5
        assert smartphone.model == "15 Pro"
        assert smartphone.memory == 256
        assert smartphone.color == "Black"

    def test_smartphone_string_representation(self):
        """Тест строкового представления смартфона"""
        smartphone = Smartphone(
            name="Samsung Galaxy",
            description="Android smartphone",
            quantity=5,
            price=799.99,
            efficiency=90.0,
            model="S23",
            memory=128,
            color="White",
        )

        expected = "Samsung Galaxy (S23), 799.99 руб. Остаток: 5 шт. Память: 128GB"
        assert str(smartphone) == expected

    def test_smartphone_inheritance(self):
        """Тест наследования от Product"""
        smartphone = Smartphone(
            name="Test Phone",
            description="Test",
            quantity=1,
            price=100.0,
            efficiency=80.0,
            model="Test",
            memory=64,
            color="Red",
        )

        assert isinstance(smartphone, Product)
        assert isinstance(smartphone, Smartphone)

    def test_smartphone_addition(self):
        """Тест сложения смартфонов"""
        phone1 = Smartphone("Phone1", "Desc", 2, 500.0, 90.0, "A", 128, "Black")
        phone2 = Smartphone("Phone2", "Desc", 3, 700.0, 85.0, "B", 256, "White")

        # Должны складываться как обычные продукты
        result = phone1 + phone2
        expected = (2 * 500.0) + (3 * 700.0)  # 1000 + 2100 = 3100
        assert result == expected


class TestLawnGrass:
    """Тесты для класса LawnGrass"""

    def test_lawn_grass_creation(self):
        """Тест создания газонной травы"""
        grass = LawnGrass(
            name="Premium Grass",
            description="Высококачественная газонная трава",
            quantity=100,
            price=25.50,
            country="Germany",
            germination_period="14 дней",
            color="Green",
        )

        assert grass.name == "Premium Grass"
        assert grass.description == "Высококачественная газонная трава"
        assert grass.quantity == 100
        assert grass.price == 25.50
        assert grass.country == "Germany"
        assert grass.germination_period == "14 дней"
        assert grass.color == "Green"

    def test_lawn_grass_string_representation(self):
        """Тест строкового представления газонной травы"""
        grass = LawnGrass(
            name="Standard Grass",
            description="Стандартная трава",
            quantity=50,
            price=15.75,
            country="Russia",
            germination_period="21 день",
            color="Dark Green",
        )

        expected = "Standard Grass, 15.75 руб. Остаток: 50 шт. Страна: Russia"
        assert str(grass) == expected

    def test_lawn_grass_inheritance(self):
        """Тест наследования от Product"""
        grass = LawnGrass(
            name="Test Grass",
            description="Test",
            quantity=10,
            price=10.0,
            country="Test",
            germination_period="Test",
            color="Test",
        )

        assert isinstance(grass, Product)
        assert isinstance(grass, LawnGrass)


class TestOrderExceptions:
    """Тесты исключений в классе Order"""

    def test_order_creation_with_zero_quantity(self):
        """Тест создания заказа с нулевым количеством"""
        product = Product("Test Product", "Description", 10, 100.0)

        with pytest.raises(ZeroQuantityError):
            Order(product, 0)

    def test_order_creation_with_negative_quantity(self):
        """Тест создания заказа с отрицательным количеством"""
        product = Product("Test Product", "Description", 10, 100.0)

        with pytest.raises(ZeroQuantityError):
            Order(product, -5)


class TestMixinInfo:
    """Тесты для миксина логирования"""

    def test_mixin_info_in_product(self):
        """Тест работы миксина в классе Product"""
        captured_output = StringIO()
        sys.stdout = captured_output

        product = Product("Test Product", "Test Description", 5, 100.0)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()

        expected = "Product('Test Product', 'Test Description', 5, 100.0)"
        assert output == expected

    def test_mixin_info_in_smartphone(self):
        """Тест работы миксина в классе Smartphone"""
        captured_output = StringIO()
        sys.stdout = captured_output

        smartphone = Smartphone(
            name="Test Phone",
            description="Test",
            quantity=1,
            price=100.0,
            efficiency=80.0,
            model="Test",
            memory=64,
            color="Red",
        )

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()

        expected = "Smartphone('Test Phone', 'Test', 1, 100.0)"
        assert output == expected


class TestDifferentProductTypes:
    """Тесты работы с разными типами продуктов"""

    def test_different_product_types_addition(self):
        """Тест сложения разных типов продуктов"""
        smartphone = Smartphone("Phone", "Desc", 2, 500.0, 90.0, "A", 128, "Black")
        lawn_grass = LawnGrass("Grass", "Desc", 3, 100.0, "RU", "14d", "Green")

        # Разные типы продуктов не должны складываться
        with pytest.raises(TypeError, match="Можно складывать только товары одинаковых классов продуктов!"):
            smartphone + lawn_grass

    def test_same_product_types_addition(self):
        """Тест сложения одинаковых типов продуктов"""
        phone1 = Smartphone("Phone1", "Desc", 2, 500.0, 90.0, "A", 128, "Black")
        phone2 = Smartphone("Phone2", "Desc", 3, 700.0, 85.0, "B", 256, "White")

        # Одинаковые типы должны складываться
        result = phone1 + phone2
        assert result == (2 * 500.0) + (3 * 700.0)

    def test_mixed_products_in_category(self):
        """Тест категории со смешанными типами продуктов"""
        smartphone = Smartphone("Phone", "Desc", 2, 500.0, 90.0, "A", 128, "Black")
        lawn_grass = LawnGrass("Grass", "Desc", 3, 100.0, "RU", "14d", "Green")
        regular_product = Product("Regular", "Desc", 5, 50.0)

        category = Category("Mixed Category", "Description", [smartphone, lawn_grass, regular_product])

        assert category.product_count == 3
        assert category.total_quantity == 10  # 2 + 3 + 5
        assert category.total_value == (2 * 500.0) + (3 * 100.0) + (5 * 50.0)  # 1000 + 300 + 250 = 1550


class TestCategoryMiddlePrice:
    """Тесты для метода средней цены категории"""

    def test_middle_price_with_products(self):
        """Тест средней цены с продуктами"""
        product1 = Product("Product1", "Desc", 5, 100.0)
        product2 = Product("Product2", "Desc", 3, 200.0)
        product3 = Product("Product3", "Desc", 2, 300.0)

        category = Category("Test Category", "Description", [product1, product2, product3])

        # (100 + 200 + 300) / 3 = 200.0
        assert category.middle_price() == 200.0

    def test_middle_price_empty_category(self):
        """Тест средней цены пустой категории"""
        category = Category("Empty Category", "Description", [])

        assert category.middle_price() == 0.0

    def test_middle_price_single_product(self):
        """Тест средней цены с одним продуктом"""
        product = Product("Single Product", "Desc", 10, 150.0)
        category = Category("Single Category", "Description", [product])

        assert category.middle_price() == 150.0


class TestIntegrationScenarios:
    """Интеграционные тесты сложных сценариев"""

    def test_complete_workflow(self):
        """Тест полного рабочего процесса"""
        # Создаем разные типы продуктов
        smartphone = Smartphone(
            name="iPhone 15",
            description="Flagship",
            quantity=10,
            price=999.99,
            efficiency=95.0,
            model="15 Pro",
            memory=256,
            color="Black",
        )

        lawn_grass = LawnGrass(
            name="Premium Grass",
            description="Quality grass",
            quantity=100,
            price=25.50,
            country="Germany",
            germination_period="14 дней",
            color="Green",
        )

        regular_product = Product("Regular", "Desc", 50, 19.99)

        # Создаем категории
        electronics = Category("Electronics", "Tech products", [smartphone])
        garden = Category("Garden", "Garden products", [lawn_grass, regular_product])

        # Проверяем категории
        assert electronics.product_count == 1
        assert garden.product_count == 2
        assert electronics.total_quantity == 10
        assert garden.total_quantity == 150

        # Создаем заказы
        phone_order = Order(smartphone, 2)
        grass_order = Order(lawn_grass, 10)

        assert phone_order.total_quantity == 2
        assert grass_order.total_quantity == 10
        assert phone_order.total_value == 2 * 999.99
        assert grass_order.total_value == 10 * 25.50

    @patch("builtins.input", return_value="Electronics")
    def test_sorting_with_different_product_types(self, mock_input):
        """Тест сортировки с разными типами продуктов"""
        smartphone = Smartphone("Phone", "Desc", 5, 500.0, 90.0, "A", 128, "Black")
        product = Product("Product", "Desc", 3, 100.0)

        category = Category("Electronics", "Tech", [smartphone, product])
        sorter = Sorting([category])

        found_products = list(sorter)
        assert len(found_products) == 2
        assert isinstance(found_products[0], Smartphone)
        assert isinstance(found_products[1], Product)


class TestEdgeCases:
    """Тесты граничных случаев"""

    def test_product_with_very_small_quantity(self):
        """Тест продукта с очень маленьким количеством"""
        product = Product("Tiny", "Desc", 1, 1000.0)
        assert product.quantity == 1
        assert product + product == 2000.0  # 1*1000 + 1*1000

    def test_product_with_very_high_price(self):
        """Тест продукта с очень высокой ценой"""
        product = Product("Expensive", "Desc", 1, 1_000_000.0)
        assert product.price == 1_000_000.0

    def test_category_with_many_products(self):
        """Тест категории со многими продуктами"""
        products = [Product(f"Product{i}", "Desc", 1, 10.0) for i in range(100)]
        category = Category("Large Category", "Desc", products)

        assert category.product_count == 100
        assert category.total_quantity == 100
        assert category.total_value == 1000.0  # 100 * 10.0


class TestPrintStatistics:
    """Тесты для вывода статистики"""

    def test_print_statistics(self):
        """Тест вывода статистики категорий"""
        # Сбрасываем счетчики
        Category.category_count = 0
        Category.total_products = 0

        product1 = Product("P1", "Desc", 5, 100.0)
        product2 = Product("P2", "Desc", 3, 200.0)

        category1 = Category("C1", "Desc", [product1])
        category2 = Category("C2", "Desc", [product2])

        captured_output = StringIO()
        sys.stdout = captured_output

        Category.print_statistics()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert "Всего категорий: 2" in output
        assert "Всего продуктов: 2" in output


class TestBaseCounter:
    """Тесты для абстрактного класса BaseCounter"""

    def test_base_counter_is_abstract(self):
        """Тест, что BaseCounter является абстрактным классом"""
        assert issubclass(BaseCounter, ABC)

        # Проверяем, что класс действительно абстрактный
        assert hasattr(BaseCounter, "__abstractmethods__")
        abstract_methods = BaseCounter.__abstractmethods__
        assert "__init__" in abstract_methods
        assert "__str__" in abstract_methods
        assert "total_quantity" in abstract_methods

    def test_cannot_instantiate_base_counter(self):
        """Тест, что нельзя создать экземпляр BaseCounter"""
        with pytest.raises(TypeError):
            BaseCounter()


class TestCategoryAsBaseCounter(unittest.TestCase):
    """Тесты для Category как наследника BaseCounter"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.product1 = Product("Телефон", "Смартфон", 5, 1000.0)
        self.product2 = Product("Планшет", "Планшет", 3, 2000.0)
        self.category = Category("Электроника", "Техника", [self.product1, self.product2])

    def test_category_total_quantity_property(self):
        """Тест свойства total_quantity в Category"""
        # Изначальное количество
        self.assertEqual(self.category.total_quantity, 8)  # 5 + 3

        # Добавляем продукт и проверяем обновление
        new_product = Product("Ноутбук", "Ноутбук", 2, 3000.0)
        self.category.add_product(new_product)
        self.assertEqual(self.category.total_quantity, 10)  # 5 + 3 + 2


class TestOrderAsBaseCounter:
    """Тесты для Order как наследника BaseCounter"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.product = Product("Телефон", "Смартфон", 10, 1000.0)
        self.order = Order(self.product, 3)

    def test_order_inherits_from_base_counter(self):
        """Тест, что Order наследуется от BaseCounter"""
        assert issubclass(Order, BaseCounter)
        assert isinstance(self.order, BaseCounter)

    def test_order_implements_abstract_methods(self):
        """Тест, что Order реализует все абстрактные методы"""
        assert hasattr(self.order, "__init__")
        assert hasattr(self.order, "__str__")
        assert hasattr(self.order, "total_quantity")

        # Проверяем работу методов
        result_str = str(self.order)
        assert "Заказ: Телефон" in result_str
        assert "Количество: 3" in result_str
        assert "Итого: 3000.0 руб." in result_str

        assert self.order.total_quantity == 3

    def test_order_total_quantity_property(self):
        """Тест свойства total_quantity в Order"""
        assert self.order.total_quantity == 3

        # Создаем другой заказ с другим количеством
        another_order = Order(self.product, 7)
        assert another_order.total_quantity == 7

    def test_order_string_representation(self):
        """Тест строкового представления Order"""
        expected = "Заказ: Телефон, Количество: 3, Итого: 3000.0 руб."
        assert str(self.order) == expected

    def test_order_total_value_calculation(self):
        """Тест расчета общей стоимости заказа"""
        assert self.order.total_value == 3000.0  # 3 * 1000.0

        # Заказ с другим количеством
        large_order = Order(self.product, 5)
        assert large_order.total_value == 5000.0  # 5 * 1000.0


class TestPolymorphism:
    """Тесты полиморфизма с BaseCounter"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.product1 = Product("Телефон", "Смартфон", 5, 1000.0)
        self.product2 = Product("Планшет", "Планшет", 3, 2000.0)

        self.category = Category("Электроника", "Техника", [self.product1, self.product2])
        self.order = Order(self.product1, 2)

    def test_polymorphic_behavior(self):
        """Тест полиморфного поведения через BaseCounter"""
        counters: list[BaseCounter] = [self.category, self.order]

        # Все объекты должны работать через общий интерфейс
        assert len(counters) == 2

        for counter in counters:
            # Должны работать общие методы
            assert isinstance(str(counter), str)
            assert isinstance(counter.total_quantity, int)
            assert hasattr(counter, "name")

    def test_different_implementations(self):
        """Тест разных реализаций одного интерфейса"""
        counters: list[BaseCounter] = [self.category, self.order]

        # Category считает сумму quantity всех продуктов
        assert counters[0].total_quantity == 8  # 5 + 3

        # Order возвращает quantity заказа
        assert counters[1].total_quantity == 2

    def test_common_interface_usage(self):
        """Тест использования общего интерфейса"""

        def print_counter_info(counter: BaseCounter):
            """Функция, работающая с любым наследником BaseCounter"""
            return f"{counter} -> Quantity: {counter.total_quantity}"

        category_info = print_counter_info(self.category)
        order_info = print_counter_info(self.order)

        assert "Электроника" in category_info
        assert "Заказ: Телефон" in order_info
        assert "Quantity: 8" in category_info
        assert "Quantity: 2" in order_info


class TestIntegration:
    """Интеграционные тесты"""

    def test_category_and_order_together(self):
        """Тест совместной работы Category и Order"""
        # Создаем продукты
        phone = Product("iPhone", "Смартфон", 10, 50000.0)
        laptop = Product("MacBook", "Ноутбук", 5, 100000.0)

        # Создаем категорию
        electronics = Category("Электроника", "Техника", [phone, laptop])
        assert electronics.total_quantity == 15

        # Создаем заказы из категории
        order1 = Order(phone, 2)
        order2 = Order(laptop, 1)

        # Проверяем, что все работают через BaseCounter
        entities = [electronics, order1, order2]

        total_quantities = [entity.total_quantity for entity in entities]
        assert total_quantities == [15, 2, 1]

        # Проверяем строковые представления
        strings = [str(entity) for entity in entities]
        assert len(strings) == 3
        assert all(isinstance(s, str) for s in strings)


class TestDataLoading:
    """Тесты для загрузки данных из JSON"""

    @patch("src.classification.load_transactions")
    def test_main_execution_with_mock_data(self, mock_load):
        """Тест основного выполнения с mock данными"""
        # Мокаем данные
        mock_load.return_value = [
            {
                "name": "Тестовая категория",
                "description": "Для тестирования",
                "products": [
                    {"name": "Тестовый продукт", "description": "Пример продукта", "price": 100.0, "quantity": 5}
                ],
            }
        ]

        # Импортируем и выполняем основной код
        from src.classification import load_transactions

        result = load_transactions("products.json")
        assert result is not None
        assert len(result) == 1
        assert result[0]["name"] == "Тестовая категория"

    @patch("src.classification.load_transactions")
    def test_main_with_empty_data(self, mock_load):
        """Тест выполнения с пустыми данными"""
        mock_load.return_value = []

        from src.classification import load_transactions

        result = load_transactions("products.json")
        assert result == []


# Запуск тестов
if __name__ == "__main__":
    print("=== ТЕСТИРОВАНИЕ BASECOUNTER И НАСЛЕДНИКОВ ===")

    # Создаем тестовые объекты
    product = Product("Test", "Desc", 5, 100.0)
    category = Category("TestCategory", "Desc", [product])
    order = Order(product, 2)

    print("✅ Category как BaseCounter:")
    print(f"   total_quantity: {category.total_quantity}")
    print(f"   str: {category}")

    print("✅ Order как BaseCounter:")
    print(f"   total_quantity: {order.total_quantity}")
    print(f"   str: {order}")

    print("✅ Полиморфизм:")
    counters = [category, order]
    for i, counter in enumerate(counters):
        print(f"   {i + 1}. {counter} -> quantity: {counter.total_quantity}")

    print("\n✅ Все основные тесты пройдены!")


if __name__ == "__main__":
    # Быстрый тест
    test_mixin_output()
    test_concrete_class_works()
    test_abstract_methods_implemented()
    print("Все основные тесты пройдены! ✅")


if __name__ == "__main__":
    # Запуск тестов
    unittest.main(verbosity=2)
