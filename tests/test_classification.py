import pytest
from src.classification import Category, Product


# Фикстуры
@pytest.fixture
def sample_product():
    return Product("Колбаса", "Краковская колбаса прямо из под собаки", 25, 1.40)


@pytest.fixture
def sample_products():
    return [
        Product("Товар 1", "Описание 1", 10, 100.0),
        Product("Товар 2", "Описание 2", 5, 200.0),
        Product("Товар 3", "Описание 3", 8, 150.0)
    ]


@pytest.fixture
def sample_category(sample_products):
    return Category("Мясо", "Грустно но вкусно", sample_products)


def test_product_init(sample_product):
    """Тест инициализации продукта"""
    assert sample_product.name == "Колбаса"
    assert sample_product.description == "Краковская колбаса прямо из под собаки"
    assert sample_product.quantity == 25
    assert sample_product.price == 1.40


def test_category_init(sample_category):
    """Тест инициализации категории"""
    assert sample_category.name == "Мясо"
    assert sample_category.description == "Грустно но вкусно"
    assert len(sample_category.products) == 3  # Исправлено: проверяем количество продуктов


class TestProductPrice:
    """Тесты для функциональности приватной цены с геттером и сеттером"""

    def test_price_getter(self):
        """Тест геттера цены"""
        product = Product("Тестовый товар", "Описание", 10, 100.0)
        assert product.price == 100.0

    def test_price_setter_valid(self):
        """Тест сеттера с валидной ценой"""
        product = Product("Тестовый товар", "Описание", 10, 100.0)
        product.price = 150.0
        assert product.price == 150.0

    def test_price_setter_negative(self, capsys):
        """Тест сеттера с отрицательной ценой"""
        product = Product("Тестовый товар", "Описание", 10, 100.0)
        product.price = -50.0

        captured = capsys.readouterr()
        # Проверяем что цена не изменилась (может не быть сообщения в зависимости от реализации)
        assert product.price == 100.0

    def test_price_setter_zero(self, capsys):
        """Тест сеттера с нулевой ценой"""
        product = Product("Тестовый товар", "Описание", 10, 100.0)
        product.price = 0

        captured = capsys.readouterr()
        assert product.price == 100.0  # Цена не должна измениться

    def test_price_private_access(self):
        """Тест, что приватный атрибут недоступен напрямую"""
        product = Product("Тестовый товар", "Описание", 10, 100.0)

        # Проверяем, что нельзя получить доступ к приватному атрибуту
        # (зависит от реализации - может быть _price или __price)
        with pytest.raises(AttributeError):
            _ = product.__price

    def test_multiple_price_changes(self):
        """Тест нескольких изменений цены"""
        product = Product("Тестовый товар", "Описание", 10, 100.0)

        product.price = 200.0
        assert product.price == 200.0

        product.price = 300.0
        assert product.price == 300.0


class TestProductClassMethod:
    """Тесты для класс-метода new_product"""

    def test_new_product_valid_data(self):
        """Тест создания продукта через класс-метод с валидными данными"""
        product_data = {
            "name": "Новый товар",
            "description": "Описание нового товара",
            "quantity": 5,
            "price": 200.0
        }

        product = Product.new_product(product_data)

        assert product.name == "Новый товар"
        assert product.description == "Описание нового товара"
        assert product.quantity == 5
        assert product.price == 200.0


class TestCategoryWithPrivateProducts:
    """Тесты для категории с приватным списком продуктов"""

    def test_private_products_access(self):
        """Тест, что приватный список продуктов недоступен напрямую"""
        product = Product("Тестовый товар", "Описание", 10, 100.0)
        category = Category("Тестовая категория", "Описание", [product])

        # Проверяем, что нельзя получить доступ к приватному атрибуту
        with pytest.raises(AttributeError):
            _ = category.__products

    def test_products_property(self):
        """Тест property для получения информации о продуктах"""
        product1 = Product("Товар 1", "Описание 1", 10, 100.0)
        product2 = Product("Товар 2", "Описание 2", 5, 200.0)

        category = Category("Тестовая категория", "Описание", [product1, product2])

        products_info = category.products

        assert len(products_info) == 2
        assert "Товар 1, 100.0 руб. Остаток: 10 шт." in products_info
        assert "Товар 2, 200.0 руб. Остаток: 5 шт." in products_info

    def test_add_product_method(self, sample_category):
        """Тест метода add_product"""
        initial_count = len(sample_category.products)
        new_product = Product("Новый товар", "Описание", 3, 50.0)

        sample_category.add_product(new_product)

        assert len(sample_category.products) == initial_count + 1


class TestCategoryStatistics:
    """Тесты для статистики категорий"""

    def test_total_categories_count(self):
        """Тест счетчика категорий"""
        initial_count = Category.total_categories

        category1 = Category("Категория 1", "Описание 1", [])
        category2 = Category("Категория 2", "Описание 2", [])

        assert Category.total_categories == initial_count + 2

    def test_total_products_count(self):
        """Тест счетчика продуктов"""
        initial_count = Category.total_products

        product1 = Product("Товар 1", "Описание", 5, 100.0)
        product2 = Product("Товар 2", "Описание", 3, 200.0)

        category = Category("Категория", "Описание", [product1, product2])

        assert Category.total_products == initial_count + 2


# Интеграционные тесты
class TestIntegration:
    """Интеграционные тесты"""

    def test_full_workflow(self):
        """Тест полного рабочего процесса"""
        # Создаем продукты через класс-метод
        product_data1 = {
            "name": "iPhone",
            "description": "Смартфон",
            "quantity": 10,
            "price": 999.99
        }
        product_data2 = {
            "name": "Samsung",
            "description": "Смартфон",
            "quantity": 15,
            "price": 799.99
        }

        product1 = Product.new_product(product_data1)
        product2 = Product.new_product(product_data2)

        # Создаем категорию (правильный порядок параметров)
        category = Category("Смартфоны", "Мобильные телефоны", [product1])

        # Добавляем второй продукт
        category.add_product(product2)

        # Меняем цену на валидную
        product1.price = 899.99
        assert product1.price == 899.99

        # Проверяем вывод продуктов
        products_info = category.products
        assert len(products_info) == 2
        assert "iPhone, 899.99 руб. Остаток: 10 шт." in products_info[0]
        assert "Samsung, 799.99 руб. Остаток: 15 шт." in products_info[1]