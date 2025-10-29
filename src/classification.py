from typing import Any

from src.utils import load_transactions


class Product:
    """Класс описания свойств продукта"""

    def __init__(self, name: str, description: str, quantity: float, price: float):
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

    def __add__(self, other):
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product!")
        return (self.price * self.quantity) + (other.price * other.quantity)


class Category:
    """Класс категорий продукта"""

    category_count = 0
    total_products = 0

    def __init__(self, name: str, description: str, products: list[Any]):
        self.name = name
        self.description = description
        self.__products = products if products is not None else []

        # Автоматически обновляем атрибуты класса при создании объекта
        Category.category_count += 1
        Category.total_products += len(self.__products)

    def add_product(self, product):
        """Добавляет продукт в категорию"""
        self.__products.append(product)
        Category.total_products += 1

    @property
    def products(self):
        """Геттер для вывода списка товаров в нужном формате"""
        return [str(product) for product in self.__products]

    def get_products_objects(self):
        """Геттер для получения списка объектов продуктов"""
        return self.__products

    @property
    def product_count(self):
        """Возвращает количество продуктов в категории"""
        return len(self.__products)

    @property
    def total_quantity(self):
        """Возвращает общее количество товаров на складе в этой категории"""
        return sum(product.quantity for product in self.__products)

    @classmethod
    def print_statistics(cls):
        """Метод для вывода статистики категорий и продуктов"""
        print(f"Всего категорий: {cls.category_count}")
        print(f"Всего продуктов: {cls.total_products}")

    def __str__(self):
        return f"{self.name}, количество продуктов: {self.total_quantity} шт."

    @property
    def total_value(self):
        """Возвращает общую стоимость всех товаров в категории"""
        return sum(product.price * product.quantity for product in self.__products)


class Sorting:
    """Класс сортировки продуктов по выбранной категории"""

    def __init__(self, categories: list[Category]):
        self.categories = categories
        self.need_find = input("Ввести категорию для сортировки продуктов: ")
        self.current_index = 0
        self.found_products = []

        # Находим все продукты в указанной категории
        for category in categories:
            if category.name.lower() == self.need_find.lower():
                self.found_products = category.get_products_objects()
                break

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index < len(self.found_products):
            product = self.found_products[self.current_index]
            self.current_index += 1
            return product
        else:
            raise StopIteration

    def print_sorted_products(self):
        """Вывод отсортированных продуктов"""
        if not self.found_products:
            print(f"Категория '{self.need_find}' не найдена или пуста")
            return

        print(f"\n=== ПРОДУКТЫ В КАТЕГОРИИ '{self.need_find}' ===")
        for product in self.found_products:
            print(f"- {product}")


if __name__ == "__main__":
    try:
        # Загружаем данные из JSON
        result = load_transactions("products.json")
        if not result:
            print("Файл products.json пуст или не найден")
            result = [
                {
                    "name": "Тестовая категория",
                    "description": "Для демонстрации",
                    "products": [
                        {"name": "Тестовый продукт", "description": "Пример продукта", "price": 100.0, "quantity": 5}
                    ],
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
                    price=product_data["price"],
                )
                category_products.append(product)

            category = Category(
                name=category_data["name"],
                description=category_data.get("description", ""),
                products=category_products,
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
