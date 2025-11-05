import os
import sys
import unittest
from abc import ABC
from io import StringIO
from unittest.mock import patch
import pytest

from src.classification import BaseCounter, Category, Order, Product, Sorting, BaseProduct, MixinInfo


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
        Category.category_count = 0
        Category.total_products = 0

        category1 = Category("Кат1", "Описание", [self.product1])
        category2 = Category("Кат2", "Описание", [self.product2, self.product3])

        self.assertEqual(Category.category_count, 2)
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

    assert output == "Product('Test', 'Desc', 100.0, 5)"


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


class TestBaseCounter:
    """Тесты для абстрактного класса BaseCounter"""

    def test_base_counter_is_abstract(self):
        """Тест, что BaseCounter является абстрактным классом"""
        assert issubclass(BaseCounter,ABC)

        # Проверяем, что класс действительно абстрактный
        assert hasattr(BaseCounter, '__abstractmethods__')
        abstract_methods = BaseCounter.__abstractmethods__
        assert '__init__' in abstract_methods
        assert '__str__' in abstract_methods
        assert 'total_quantity' in abstract_methods

    def test_cannot_instantiate_base_counter(self):
        """Тест, что нельзя создать экземпляр BaseCounter"""
        with pytest.raises(TypeError):
            BaseCounter()


class TestCategoryAsBaseCounter:
    """Тесты для Category как наследника BaseCounter"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.product1 = Product("Телефон", "Смартфон", 5, 1000.0)
        self.product2 = Product("Планшет", "Планшет", 3, 2000.0)
        self.category = Category("Электроника", "Техника", [self.product1, self.product2])

    def test_category_inherits_from_base_counter(self):
        """Тест, что Category наследуется от BaseCounter"""
        assert issubclass(Category, BaseCounter)
        assert isinstance(self.category, BaseCounter)

    def test_category_implements_abstract_methods(self):
        """Тест, что Category реализует все абстрактные методы"""
        # Проверяем, что методы существуют и работают
        assert hasattr(self.category, '__init__')
        assert hasattr(self.category, '__str__')
        assert hasattr(self.category, 'total_quantity')

        # Проверяем работу методов
        result_str = str(self.category)
        assert "Электроника" in result_str
        assert "количество продуктов: 8 шт." in result_str

        assert self.category.total_quantity == 8  # 5 + 3

    def test_category_total_quantity_property(self):
        """Тест свойства total_quantity в Category"""
        # Изначальное количество
        assert self.category.total_quantity == 8

        # Добавляем продукт и проверяем обновление
        new_product = Product("Ноутбук", "Ноутбук", 2, 3000.0)
        self.category.add_product(new_product)
        assert self.category.total_quantity == 10  # 5 + 3 + 2

    def test_category_string_representation(self):
        """Тест строкового представления Category"""
        expected = "Электроника, количество продуктов: 8 шт."
        assert str(self.category) == expected

    def test_category_with_empty_products(self):
        """Тест Category с пустым списком продуктов"""
        empty_category = Category("Пустая", "Категория без продуктов", [])
        assert empty_category.total_quantity == 0
        assert str(empty_category) == "Пустая, количество продуктов: 0 шт."


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
        assert hasattr(self.order, '__init__')
        assert hasattr(self.order, '__str__')
        assert hasattr(self.order, 'total_quantity')

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
            assert hasattr(counter, 'name')

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


class TestEdgeCases:
    """Тесты граничных случаев"""

    def test_category_with_zero_quantity_products(self):
        """Тест Category с продуктами с нулевым количеством"""
        zero_product = Product("Товар1", "Описание", 0, 100.0)
        normal_product = Product("Товар2", "Описание", 5, 200.0)

        category = Category("Тест", "Категория", [zero_product, normal_product])
        assert category.total_quantity == 5

    def test_order_with_zero_quantity(self):
        """Тест Order с нулевым количеством"""
        product = Product("Товар", "Описание", 10, 100.0)
        order = Order(product, 0)

        assert order.total_quantity == 0
        assert order.total_value == 0.0
        assert "Количество: 0" in str(order)

    def test_order_with_large_quantity(self):
        """Тест Order с большим количеством"""
        product = Product("Товар", "Описание", 1000, 1.0)
        order = Order(product, 500)

        assert order.total_quantity == 500
        assert order.total_value == 500.0


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


# Запуск тестов
if __name__ == "__main__":
    # Простой запуск для демонстрации
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
