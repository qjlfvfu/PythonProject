import pytest

from src.classification import Category, Product


def test_init(sausage):
    assert sausage.name == "Колбаса"
    assert sausage.description == "Краковская колбаса прямо из под собаки"
    assert sausage.quantity == 25
    assert sausage.price == 1.40


def test_category_init(list_category):
    assert list_category.total_products == 3
    assert list_category.name == "Мясо"
    assert list_category.description == "Грустно но вкусно"
    assert list_category.total_categories == 1


class TestProductPrice:
    """Тесты для функциональности приватной цены с геттером и сеттером"""

    def test_price_getter(self):
        """Тест геттера цены"""
        product = Product("Тестовый товар", "Описание", 10, 100.0)
        assert product.price == 100.0  # Геттер возвращает правильное значение

    def test_price_setter_valid(self):
        """Тест сеттера с валидной ценой"""
        product = Product("Тестовый товар", "Описание", 10, 100.0)
        product.price = 150.0  # Устанавливаем новую валидную цену
        assert product.price == 150.0  # Цена успешно изменилась

    def test_price_setter_negative(self, capsys):
        """Тест сеттера с отрицательной ценой"""
        product = Product("Тестовый товар", "Описание", 10, 100.0)
        product.price = -50.0  # Пытаемся установить отрицательную цену

        # Проверяем сообщение об ошибке
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        # Проверяем, что цена не изменилась
        assert product.price == 100.0

    def test_price_setter_zero(self, capsys):
        """Тест сеттера с нулевой ценой"""
        product = Product("Тестовый товар", "Описание", 10, 100.0)
        product.price = 0  # Пытаемся установить нулевую цену

        # Проверяем сообщение об ошибке
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out

        # Проверяем, что цена не изменилась
        assert product.price == 100.0

    def test_price_private_access(self):
        """Тест, что приватный атрибут недоступен напрямую"""
        product = Product("Тестовый товар", "Описание", 10, 100.0)

        # Проверяем, что нельзя получить доступ к приватному атрибуту
        with pytest.raises(AttributeError):
            _ = product.__price

    def test_multiple_price_changes(self, capsys):
        """Тест нескольких изменений цены"""
        product = Product("Тестовый товар", "Описание", 10, 100.0)

        # Валидное изменение
        product.price = 200.0
        assert product.price == 200.0

        # Невалидное изменение
        product.price = -100.0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 200.0  # Цена осталась прежней

        # Еще одно валидное изменение
        product.price = 300.0
        assert product.price == 300.0

    def test_price_in_product_info(self):
        """Тест, что цена корректно отображается в информации о продукте"""
        product = Product("Тестовый товар", "Описание", 10, 150.0)

        # Создаем категорию и добавляем продукт
        category = Category("Тестовая категория", [product], "Описание категории")

        # Проверяем, что цена отображается в списке продуктов
        product_info = category.products[0]
        assert "150.0 руб." in product_info


class TestProductClassMethod:
    """Тесты для класс-метода new_product"""

    def test_new_product_valid_data(self):
        """Тест создания продукта через класс-метод с валидными данными"""
        product_data = {"name": "Новый товар", "description": "Описание нового товара", "quantity": 5, "price": 200.0}

        product = Product.new_product(product_data)

        assert product.name == "Новый товар"
        assert product.description == "Описание нового товара"
        assert product.quantity == 5
        assert product.price == 200.0

    def test_new_product_with_negative_price(self, capsys):
        """Тест создания продукта с отрицательной ценой через класс-метод"""
        product_data = {
            "name": "Товар с отрицательной ценой",
            "description": "Описание",
            "quantity": 5,
            "price": -100.0,  # Отрицательная цена при создании
        }

        product = Product.new_product(product_data)

        # Продукт создается, но при попытке изменить цену через сеттер будет ошибка
        assert product.price == -100.0  # Прямое присвоение в __init__ работает

        # Тестируем, что сеттер блокирует дальнейшие изменения на отрицательные значения
        product.price = -50.0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == -100.0  # Осталась исходная цена (из __init__)


class TestCategoryWithPrivateProducts:
    """Тесты для категории с приватным списком продуктов"""

    def test_private_products_access(self):
        """Тест, что приватный список продуктов недоступен напрямую"""
        product = Product("Тестовый товар", "Описание", 10, 100.0)
        category = Category("Тестовая категория", [product], "Описание")

        # Проверяем, что нельзя получить доступ к приватному атрибуту
        with pytest.raises(AttributeError):
            _ = category.__products

    def test_products_property(self):
        """Тест property для получения информации о продуктах"""
        product1 = Product("Товар 1", "Описание 1", 10, 100.0)
        product2 = Product("Товар 2", "Описание 2", 5, 200.0)

        category = Category("Тестовая категория", [product1, product2], "Описание")

        products_info = category.products

        assert len(products_info) == 2
        assert "Товар 1, 100.0 руб. Остаток: 10 шт." in products_info
        assert "Товар 2, 200.0 руб. Остаток: 5 шт." in products_info

    def test_add_product_method(self):
        """Тест метода add_product"""
        product1 = Product("Товар 1", "Описание 1", 10, 100.0)
        product2 = Product("Товар 2", "Описание 2", 5, 200.0)

        category = Category("Тестовая категория", [product1], "Описание")
        initial_count = Category.total_products

        category.add_product(product2)

        # Проверяем, что продукт добавился
        assert len(category.products) == 2
        assert Category.total_products == initial_count + 1


# Дополнительные интеграционные тесты
class TestIntegration:
    """Интеграционные тесты"""

    def test_full_workflow(self, capsys):
        """Тест полного рабочего процесса"""
        # Создаем продукты через класс-метод
        product_data1 = {"name": "iPhone", "description": "Смартфон", "quantity": 10, "price": 999.99}
        product_data2 = {"name": "Samsung", "description": "Смартфон", "quantity": 15, "price": 799.99}

        product1 = Product.new_product(product_data1)
        product2 = Product.new_product(product_data2)

        # Создаем категорию
        category = Category("Смартфоны", [product1], "Мобильные телефоны")

        # Добавляем второй продукт
        category.add_product(product2)

        # Пытаемся изменить цену на невалидную
        product1.price = -500.0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product1.price == 999.99  # Цена не изменилась

        # Меняем цену на валидную
        product1.price = 899.99
        assert product1.price == 899.99

        # Проверяем вывод продуктов
        products_info = category.products
        assert len(products_info) == 2
        assert "iPhone, 899.99 руб. Остаток: 10 шт." in products_info
        assert "Samsung, 799.99 руб. Остаток: 15 шт." in products_info
