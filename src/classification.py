from src.utils import load_transactions
from typing import Any

class Product:
    """Класс описания свойств продукта"""

    def __init__(self, name: str, description: str, quantity: int, price: float):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.__price = price  # Приватный атрибут цены

    @property
    def price(self):
        """Геттер для цены"""
        return self.__price

    @price.setter
    def price(self, new_price):
        """Сеттер для цены с проверкой"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict):
        """
        Класс-метод для создания объекта Product из словаря
        """
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            quantity=product_data["quantity"],
            price=product_data["price"],
        )

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."


class Category:
    """Класс категорий продукта"""

    total_categories = 0
    total_products = 0

    def __init__(self, name: str, description: str, products: list[Any]):
        self.name = name
        self.description = description
        self.__products = products if products is not None else []

        # Автоматически обновляем атрибуты класса при создании объекта
        Category.total_categories += 1
        Category.total_products += len(self.__products)

    def add_product(self, product):
        """Добавляет продукт в категорию"""
        self.__products.append(product)
        Category.total_products += 1

    @property
    def products(self):
        """Геттер для вывода списка товаров в нужном формате"""
        products_list = []
        for product in self.__products:
            product_info = f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            products_list.append(product_info)
        return products_list

    def get_products_objects(self):
        """Геттер для получения списка объектов продуктов"""
        return self.__products

    @property
    def product_count(self):
        """Возвращает количество продуктов в категории"""
        return len(self.__products)

    @classmethod
    def print_statistics(cls):
        """Метод для вывода статистики категорий и продуктов"""
        print(f"Всего категорий: {cls.total_categories}")
        print(f"Всего продуктов: {cls.total_products}")

    def __str__(self):
        return f"Категория: {self.name}, продуктов: {self.product_count}"


if __name__ == "__main__":
    try:
        # Загружаем данные из JSON
        result = load_transactions("products.json")
        if not result:
            print("Файл products.json пуст или не найден")
            # Создаем тестовые данные
            result = [
                {
                    "name": "Тестовая категория",
                    "description": "Для демонстрации",
                    "products": [
                        {
                            "name": "Тестовый продукт",
                            "description": "Пример продукта",
                            "price": 100.0,
                            "quantity": 5
                        }
                    ]
                }
            ]

        categories = []
        for category_data in result:
            category_products = []
            for product_data in category_data["products"]:
                product = Product(
                    name=product_data["name"],
                    description=product_data.get("description", ""),
                    quantity=product_data["quantity"],
                    price=product_data["price"]
                )
                category_products.append(product)

            category = Category(
                name=category_data["name"],
                description=category_data.get("description", ""),
                products=category_products
            )
            categories.append(category)

        print("=== СОЗДАННЫЕ КАТЕГОРИИ ===")
        for category in categories:
            print(f"\n{category}")
            print(f"Описание: {category.description}")
            print("Продукты:")
            for product_info in category.products:
                print(f"  - {product_info}")

        Category.print_statistics()

        print(f"\n=== ТЕСТ ИЗМЕНЕНИЯ ЦЕН ===")
        if categories and categories[0].product_count > 0:
            # Используем новый геттер вместо прямого доступа к приватному атрибуту
            products_objects = categories[0].get_products_objects()
            if products_objects:
                product = products_objects[0]  # Получаем первый продукт
                print(f"Исходная цена: {product.price}")

                product.price = 150.0  # Валидное изменение
                print(f"После валидного изменения: {product.price}")

                product.price = -50.0  # Невалидное изменение
                print(f"После невалидного изменения: {product.price}")  # Должна остаться прежняя

    except Exception as e:
        print(f"Ошибка: {e}")