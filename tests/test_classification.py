import os
import sys
import unittest
from abc import ABC
from io import StringIO
from unittest.mock import Mock, patch

from src.classification import (BaseCounter, Category, LawnGrass, Order, Product, Smartphone, Sorting,
                                ZeroQuantityError)

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))


class TestProductFeatures(unittest.TestCase):
    """Тесты для новых возможностей класса Product"""

    def setUp(self):
        """Подготовка тестовых данных"""
        self.product1 = Product("Телефон", "Смартфон", 1000.0, 10)
        self.product2 = Product("Планшет", "Планшет", 2000.0, 5)
        self.product3 = Product("Ноутбук", "Ноутбук", 5000.0, 3)

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
        cheap_product = Product("Дешевый", "Товар", 10.0, 100)
        expensive_product = Product("Дорогой", "Товар", 1000.0, 2)

        # 100 * 10 + 2 * 1000 = 1000 + 2000 = 3000
        result = cheap_product + expensive_product
        self.assertEqual(result, 3000.0)

    def test_product_addition_type_error(self):
        """Тест ошибки типа при сложении"""
        with self.assertRaises(TypeError):
            self.product1 + "не продукт"

    def test_product_string_representation(self):
        """Тест строкового представления продукта"""
        product = Product("Тест", "Описание", 150.5, 15)
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
        self.product1 = Product("Товар1", "Описание1", 100.0, 10)
        self.product2 = Product("Товар2", "Описание2", 200.0, 5)
        self.product3 = Product("Товар3", "Описание3", 300.0, 3)

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
        self.assertEqual(self.category.product_count, 3)


class TestSortingFeatures(unittest.TestCase):
    """Тесты для класса Sorting"""

    def setUp(self):
        """Подготовка тестовых данных"""
        self.product1 = Product("iPhone", "Смартфон", 1000.0, 10)
        self.product2 = Product("Samsung", "Смартфон", 800.0, 5)
        self.product3 = Product("MacBook", "Ноутбук", 2000.0, 3)
        self.product4 = Product("ThinkPad", "Ноутбук", 1500.0, 7)

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
        product_a = Product("A", "Товар A", 100.0, 10)
        product_b = Product("B", "Товар B", 200.0, 2)

        category = Category("Тест", "Описание", [product_a, product_b])

        # Сложение продуктов из категории
        total_value = product_a + product_b
        self.assertEqual(total_value, 1400.0)  # 10*100 + 2*200 = 1400

        # Проверяем, что total_value категории совпадает
        self.assertEqual(category.total_value, 1400.0)

    def test_complex_scenario(self):
        """Тест сложного сценария со всеми функциями"""
        # Создаем продукты
        phone1 = Product("Phone1", "Смартфон", 500.0, 5)
        phone2 = Product("Phone2", "Смартфон", 700.0, 3)
        laptop1 = Product("Laptop1", "Ноутбук", 1000.0, 2)
        laptop2 = Product("Laptop2", "Ноутбук", 1500.0, 1)

        # Создаем категории
        phones_category = Category("Телефоны", "Мобильные", [phone1, phone2])
        laptops_category = Category("Ноутбуки", "Компьютеры", [laptop1, laptop2])

        # Тестируем сложение
        phone_total = phone1 + phone2  # 5*500 + 3*700 = 2500 + 2100 = 4600
        laptop_total = laptop1 + laptop2  # 2*1000 + 1*1500 = 2000 + 1500 = 3500

        self.assertEqual(phone_total, 4600.0)
        self.assertEqual(laptop_total, 3500.0)

        # Тестируем строковые представления
        self.assertEqual(str(phones_category), "Телефоны, количество продуктов: 8 шт.")
        self.assertEqual(str(laptops_category), "Ноутбуки, количество продуктов: 3 шт.")


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

        self.assertIn("создан", str(error1))
        self.assertIn("обновлен", str(error2))


class TestProductExceptions(unittest.TestCase):
    """Тесты исключений в классе Product"""

    def test_product_creation_with_zero_quantity(self):
        """Тест создания продукта с нулевым количеством"""
        with self.assertRaises(ValueError) as context:
            Product("Test Product", "Description", 100.0, 0)

        self.assertEqual(str(context.exception), "Товар с нулевым количеством не может быть добавлен")

    def test_product_creation_with_negative_quantity(self):
        """Тест создания продукта с отрицательным количеством"""
        with self.assertRaises(ValueError) as context:
            Product("Test Product", "Description", 100.0, -5)

        self.assertEqual(str(context.exception), "Товар с нулевым количеством не может быть добавлен")

    def test_product_creation_with_positive_quantity(self):
        """Тест создания продукта с положительным количеством"""
        product = Product("Test Product", "Description", 100.0, 1)
        self.assertEqual(product.quantity, 1)
        self.assertEqual(product.price, 100.0)


class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев"""

    def test_order_with_zero_quantity(self):
        """Тест Order с нулевым количеством"""
        product = Product("Товар", "Описание", 100.0, 10)

        with self.assertRaises(ZeroQuantityError) as context:
            Order(product, 0)

        self.assertEqual(str(context.exception), "Товар 'Товар' не может быть создан: количество равно нулю")

    def test_order_with_positive_quantity(self):
        """Тест Order с положительным количеством"""
        product = Product("Товар", "Описание", 100.0, 10)

        order = Order(product, 5)
        self.assertEqual(order.quantity, 5)
        self.assertEqual(order.total_value, 500.0)


class TestCategoryExceptions(unittest.TestCase):
    """Тесты исключений в классе Category"""

    def test_add_product_with_zero_quantity(self):
        """Тест добавления продукта с нулевым количеством в категорию"""
        category = Category("Test Category", "Description", [])

        # Создаем mock объект для тестирования
        mock_product = Mock(spec=Product)
        mock_product.name = "Zero Product"
        mock_product.quantity = 0

        with self.assertRaises(ZeroQuantityError) as context:
            category.add_product(mock_product)

        self.assertEqual(str(context.exception), "Товар 'Zero Product' не может быть добавлен: количество равно нулю")


class TestSmartphone(unittest.TestCase):
    """Тесты для класса Smartphone"""

    def test_smartphone_creation(self):
        """Тест создания смартфона"""
        smartphone = Smartphone(
            name="iPhone 15",
            description="Флагманский смартфон",
            price=999.99,
            quantity=10,
            efficiency=95.5,
            model="15 Pro",
            memory=256,
            color="Black",
        )

        self.assertEqual(smartphone.name, "iPhone 15")
        self.assertEqual(smartphone.description, "Флагманский смартфон")
        self.assertEqual(smartphone.quantity, 10)
        self.assertEqual(smartphone.price, 999.99)
        self.assertEqual(smartphone.efficiency, 95.5)
        self.assertEqual(smartphone.model, "15 Pro")
        self.assertEqual(smartphone.memory, 256)
        self.assertEqual(smartphone.color, "Black")

    def test_smartphone_string_representation(self):
        """Тест строкового представления смартфона"""
        smartphone = Smartphone(
            name="Samsung Galaxy",
            description="Android smartphone",
            price=799.99,
            quantity=5,
            efficiency=90.0,
            model="S23",
            memory=128,
            color="White",
        )

        expected = "Samsung Galaxy (S23), 799.99 руб. Остаток: 5 шт. Память: 128GB"
        self.assertEqual(str(smartphone), expected)

    def test_smartphone_inheritance(self):
        """Тест наследования от Product"""
        smartphone = Smartphone(
            name="Test Phone",
            description="Test",
            price=100.0,
            quantity=1,
            efficiency=80.0,
            model="Test",
            memory=64,
            color="Red",
        )

        self.assertIsInstance(smartphone, Product)
        self.assertIsInstance(smartphone, Smartphone)

    def test_smartphone_addition(self):
        """Тест сложения смартфонов"""
        phone1 = Smartphone("Phone1", "Desc", 500.0, 2, 90.0, "A", 128, "Black")
        phone2 = Smartphone("Phone2", "Desc", 700.0, 3, 85.0, "B", 256, "White")

        result = phone1 + phone2
        expected = (2 * 500.0) + (3 * 700.0)  # 1000 + 2100 = 3100
        self.assertEqual(result, expected)


class TestLawnGrass(unittest.TestCase):
    """Тесты для класса LawnGrass"""

    def test_lawn_grass_creation(self):
        """Тест создания газонной травы"""
        grass = LawnGrass(
            name="Premium Grass",
            description="Высококачественная газонная трава",
            price=25.50,
            quantity=100,
            country="Germany",
            germination_period="14 дней",
            color="Green",
        )

        self.assertEqual(grass.name, "Premium Grass")
        self.assertEqual(grass.description, "Высококачественная газонная трава")
        self.assertEqual(grass.quantity, 100)
        self.assertEqual(grass.price, 25.50)
        self.assertEqual(grass.country, "Germany")
        self.assertEqual(grass.germination_period, "14 дней")
        self.assertEqual(grass.color, "Green")

    def test_lawn_grass_string_representation(self):
        """Тест строкового представления газонной травы"""
        grass = LawnGrass(
            name="Standard Grass",
            description="Стандартная трава",
            price=15.75,
            quantity=50,
            country="Russia",
            germination_period="21 день",
            color="Dark Green",
        )

        expected = "Standard Grass, 15.75 руб. Остаток: 50 шт. Страна: Russia"
        self.assertEqual(str(grass), expected)

    def test_lawn_grass_inheritance(self):
        """Тест наследования от Product"""
        grass = LawnGrass(
            name="Test Grass",
            description="Test",
            price=10.0,
            quantity=10,
            country="Test",
            germination_period="Test",
            color="Test",
        )

        self.assertIsInstance(grass, Product)
        self.assertIsInstance(grass, LawnGrass)


class TestOrderExceptions(unittest.TestCase):
    """Тесты исключений в классе Order"""

    def test_order_creation_with_zero_quantity(self):
        """Тест создания заказа с нулевым количеством"""
        product = Product("Test Product", "Description", 100.0, 10)

        with self.assertRaises(ZeroQuantityError):
            Order(product, 0)

    def test_order_creation_with_negative_quantity(self):
        """Тест создания заказа с отрицательным количеством"""
        product = Product("Test Product", "Description", 100.0, 10)

        with self.assertRaises(ZeroQuantityError):
            Order(product, -5)


class TestMixinInfo(unittest.TestCase):
    """Тесты для миксина логирования"""

    def test_mixin_info_in_product(self):
        """Тест работы миксина в классе Product"""
        captured_output = StringIO()
        sys.stdout = captured_output

        product = Product("Test Product", "Test Description", 100.0, 5)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()

        expected = "Product('Test Product', 'Test Description', 100.0, 5)"
        self.assertEqual(output, expected)


class TestDifferentProductTypes(unittest.TestCase):
    """Тесты работы с разными типами продуктов"""

    def test_different_product_types_addition(self):
        """Тест сложения разных типов продуктов"""
        smartphone = Smartphone("Phone", "Desc", 500.0, 2, 90.0, "A", 128, "Black")
        lawn_grass = LawnGrass("Grass", "Desc", 100.0, 3, "RU", "14d", "Green")

        with self.assertRaises(TypeError) as context:
            smartphone + lawn_grass

        self.assertEqual(str(context.exception), "Можно складывать только товары одинаковых классов продуктов!")

    def test_same_product_types_addition(self):
        """Тест сложения одинаковых типов продуктов"""
        phone1 = Smartphone("Phone1", "Desc", 500.0, 2, 90.0, "A", 128, "Black")
        phone2 = Smartphone("Phone2", "Desc", 700.0, 3, 85.0, "B", 256, "White")

        result = phone1 + phone2
        self.assertEqual(result, (2 * 500.0) + (3 * 700.0))

    def test_mixed_products_in_category(self):
        """Тест категории со смешанными типами продуктов"""
        smartphone = Smartphone("Phone", "Desc", 500.0, 2, 90.0, "A", 128, "Black")
        lawn_grass = LawnGrass("Grass", "Desc", 100.0, 3, "RU", "14d", "Green")
        regular_product = Product("Regular", "Desc", 50.0, 5)

        category = Category("Mixed Category", "Description", [smartphone, lawn_grass, regular_product])

        self.assertEqual(category.product_count, 3)
        self.assertEqual(category.total_quantity, 10)  # 2 + 3 + 5
        self.assertEqual(category.total_value, (2 * 500.0) + (3 * 100.0) + (5 * 50.0))  # 1000 + 300 + 250 = 1550


class TestCategoryMiddlePrice(unittest.TestCase):
    """Тесты для метода средней цены категории"""

    def test_middle_price_with_products(self):
        """Тест средней цены с продуктами"""
        product1 = Product("Product1", "Desc", 100.0, 5)
        product2 = Product("Product2", "Desc", 200.0, 3)
        product3 = Product("Product3", "Desc", 300.0, 2)

        category = Category("Test Category", "Description", [product1, product2, product3])

        # (100 + 200 + 300) / 3 = 200.0
        self.assertEqual(category.middle_price(), 200.0)

    def test_middle_price_empty_category(self):
        """Тест средней цены пустой категории"""
        category = Category("Empty Category", "Description", [])

        self.assertEqual(category.middle_price(), 0.0)

    def test_middle_price_single_product(self):
        """Тест средней цены с одним продуктом"""
        product = Product("Single Product", "Desc", 150.0, 10)
        category = Category("Single Category", "Description", [product])

        self.assertEqual(category.middle_price(), 150.0)


class TestBaseCounter(unittest.TestCase):
    """Тесты для абстрактного класса BaseCounter"""

    def test_base_counter_is_abstract(self):
        """Тест, что BaseCounter является абстрактным классом"""
        self.assertTrue(issubclass(BaseCounter, ABC))

    def test_cannot_instantiate_base_counter(self):
        """Тест, что нельзя создать экземпляр BaseCounter"""
        with self.assertRaises(TypeError):
            BaseCounter()


class TestCategoryAsBaseCounter(unittest.TestCase):
    """Тесты для Category как наследника BaseCounter"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.product1 = Product("Телефон", "Смартфон", 1000.0, 5)
        self.product2 = Product("Планшет", "Планшет", 2000.0, 3)
        self.category = Category("Электроника", "Техника", [self.product1, self.product2])

    def test_category_total_quantity_property(self):
        """Тест свойства total_quantity в Category"""
        self.assertEqual(self.category.total_quantity, 8)  # 5 + 3

        new_product = Product("Ноутбук", "Ноутбук", 3000.0, 2)
        self.category.add_product(new_product)
        self.assertEqual(self.category.total_quantity, 10)  # 5 + 3 + 2


class TestOrderAsBaseCounter(unittest.TestCase):
    """Тесты для Order как наследника BaseCounter"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.product = Product("Телефон", "Смартфон", 1000.0, 10)
        self.order = Order(self.product, 3)

    def test_order_inherits_from_base_counter(self):
        """Тест, что Order наследуется от BaseCounter"""
        self.assertTrue(issubclass(Order, BaseCounter))
        self.assertIsInstance(self.order, BaseCounter)

    def test_order_implements_abstract_methods(self):
        """Тест, что Order реализует все абстрактные методы"""
        self.assertTrue(hasattr(self.order, "__init__"))
        self.assertTrue(hasattr(self.order, "__str__"))
        self.assertTrue(hasattr(self.order, "total_quantity"))

        result_str = str(self.order)
        self.assertIn("Заказ: Телефон", result_str)
        self.assertIn("Количество: 3", result_str)
        self.assertIn("Итого: 3000.0 руб.", result_str)

        self.assertEqual(self.order.total_quantity, 3)

    def test_order_total_quantity_property(self):
        """Тест свойства total_quantity в Order"""
        self.assertEqual(self.order.total_quantity, 3)

        another_order = Order(self.product, 7)
        self.assertEqual(another_order.total_quantity, 7)

    def test_order_string_representation(self):
        """Тест строкового представления Order"""
        expected = "Заказ: Телефон, Количество: 3, Итого: 3000.0 руб."
        self.assertEqual(str(self.order), expected)

    def test_order_total_value_calculation(self):
        """Тест расчета общей стоимости заказа"""
        self.assertEqual(self.order.total_value, 3000.0)  # 3 * 1000.0

        large_order = Order(self.product, 5)
        self.assertEqual(large_order.total_value, 5000.0)  # 5 * 1000.0


class TestPolymorphism(unittest.TestCase):
    """Тесты полиморфизма с BaseCounter"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.product1 = Product("Телефон", "Смартфон", 1000.0, 5)
        self.product2 = Product("Планшет", "Планшет", 2000.0, 3)

        self.category = Category("Электроника", "Техника", [self.product1, self.product2])
        self.order = Order(self.product1, 2)

    def test_polymorphic_behavior(self):
        """Тест полиморфного поведения через BaseCounter"""
        counters = [self.category, self.order]

        self.assertEqual(len(counters), 2)

        for counter in counters:
            self.assertIsInstance(str(counter), str)
            self.assertIsInstance(counter.total_quantity, int)
            self.assertTrue(hasattr(counter, "name"))

    def test_different_implementations(self):
        """Тест разных реализаций одного интерфейса"""
        counters = [self.category, self.order]

        # Category считает сумму quantity всех продуктов
        self.assertEqual(counters[0].total_quantity, 8)  # 5 + 3

        # Order возвращает quantity заказа
        self.assertEqual(counters[1].total_quantity, 2)


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""

    def test_category_and_order_together(self):
        """Тест совместной работы Category и Order"""
        # Создаем продукты
        phone = Product("iPhone", "Смартфон", 50000.0, 10)
        laptop = Product("MacBook", "Ноутбук", 100000.0, 5)

        # Создаем категорию
        electronics = Category("Электроника", "Техника", [phone, laptop])
        self.assertEqual(electronics.total_quantity, 15)

        # Создаем заказы из категории
        order1 = Order(phone, 2)
        order2 = Order(laptop, 1)

        # Проверяем, что все работают через BaseCounter
        entities = [electronics, order1, order2]

        total_quantities = [entity.total_quantity for entity in entities]
        self.assertEqual(total_quantities, [15, 2, 1])

        # Проверяем строковые представления
        strings = [str(entity) for entity in entities]
        self.assertEqual(len(strings), 3)
        self.assertTrue(all(isinstance(s, str) for s in strings))


class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев"""

    def test_product_with_very_small_quantity(self):
        """Тест продукта с очень маленьким количеством"""
        product = Product("Tiny", "Desc", 1000.0, 1)
        self.assertEqual(product.quantity, 1)
        self.assertEqual(product + product, 2000.0)  # 1*1000 + 1*1000

    def test_product_with_very_high_price(self):
        """Тест продукта с очень высокой ценой"""
        product = Product("Expensive", "Desc", 1000000.0, 1)
        self.assertEqual(product.price, 1000000.0)

    def test_category_with_many_products(self):
        """Тест категории со многими продуктами"""
        products = [Product(f"Product{i}", "Desc", 10.0, 1) for i in range(100)]
        category = Category("Large Category", "Desc", products)

        self.assertEqual(category.product_count, 100)
        self.assertEqual(category.total_quantity, 100)
        self.assertEqual(category.total_value, 1000.0)  # 100 * 10.0


class TestPrintStatistics(unittest.TestCase):
    """Тесты для вывода статистики"""

    def test_print_statistics(self):
        """Тест вывода статистики категорий"""
        # Сбрасываем счетчики
        Category.category_count = 0
        Category.total_products = 0

        product1 = Product("P1", "Desc", 100.0, 5)
        product2 = Product("P2", "Desc", 200.0, 3)

        category1 = Category("C1", "Desc", [product1])
        category2 = Category("C2", "Desc", [product2])

        captured_output = StringIO()
        sys.stdout = captured_output

        Category.print_statistics()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Всего категорий: 2", output)
        self.assertIn("Всего продуктов: 2", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
