from abc import ABC, abstractmethod
from typing import Any

from src.utils import load_transactions


class MixinInfo:
    """Миксин для логирования создания объектов"""

    def __init__(self, *args, **kwargs):
        """Инициализация с логированием создания объекта"""
        super().__init__(*args, **kwargs)
        print(
            f"{self.__class__.__name__}('{getattr(self, 'name', '')}', '{getattr(self, 'description', '')}',"
            f" {getattr(self, 'price', 0)}, {getattr(self, 'quantity', 0)})"
        )


class BaseProduct(ABC, MixinInfo):
    """Абстрактный базовый класс для всех продуктов"""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: float):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        super().__init__()

    @abstractmethod
    def __add__(self, other):
        """Абстрактный метод сложения продуктов"""
        pass

    @abstractmethod
    def __str__(self):
        """Абстрактный метод строкового представления"""
        pass


class Product(BaseProduct):
    """Класс описания свойств продукта"""

    def __init__(self, name: str, description: str, price: float, quantity: float):
        if quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        super().__init__(name, description, price, quantity)

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
        if product_data["quantity"] <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Метод определяющий принадлежность к другой категории
        и запрещающий добавлять предметы других категорий"""
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product!")
        if type(self) is not type(other):
            raise TypeError("Можно складывать только товары одинаковых классов продуктов!")

        return (self.price * self.quantity) + (other.price * other.quantity)


class BaseCounter(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @property
    @abstractmethod
    def total_quantity(self) -> int:
        pass


class Category(BaseCounter):
    """Класс категорий продукта"""

    category_count = 0
    total_products = 0

    def __init__(self, name: str, description: str, products: list[Any]):
        self.name = name
        self.description = description
        self.__products = products if products is not None else []
        super().__init__()

        Category.category_count += 1
        Category.total_products += len(self.__products)

    def add_product(self, product):
        """Добавляет продукт в категорию с обработкой исключений"""
        product_name = getattr(product, "name", "неизвестный товар")

        try:
            print(f"\n🔄 Начало обработки добавления товара '{product_name}' в категорию '{self.name}'")

            if not isinstance(product, Product):
                raise TypeError("Можно добавлять только объекты класса Product")

            if product.quantity <= 0:
                raise ZeroQuantityError(product.name, "добавлен")

            self.__products.append(product)
            Category.total_products += 1

            print(f"✅ Товар '{product_name}' успешно добавлен в категорию '{self.name}'")

        except (TypeError, ZeroQuantityError) as e:
            print(f"❌ Ошибка при добавлении товара: {e}")
            raise
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
            raise
        finally:
            print(f"🏁 Обработка добавления товара '{product_name}' завершена")

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

    def middle_price(self) -> float:
        """
        Возвращает среднюю цену всех товаров в категории.
        Если в категории нет товаров, возвращает 0.
        """
        try:
            if not self.__products:
                return 0.0

            total_price = sum(product.price for product in self.__products)
            average_price = total_price / len(self.__products)
            return round(average_price, 2)

        except ZeroDivisionError:
            return 0.0

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


class Order(BaseCounter):
    """Класс для работы с заказами"""

    def __init__(self, product, quantity):
        product_name = product.name

        try:
            print(f"\n🔄 Начало обработки создания заказа для товара '{product_name}'")

            if quantity <= 0:
                raise ZeroQuantityError(product_name, "создан")

            self.product = product
            self.quantity = quantity
            self.total_value = product.price * quantity
            self.name = f"Заказ {product_name}"

            print(f"✅ Заказ для товара '{product_name}' успешно создан")

        except ZeroQuantityError as e:
            print(f"❌ Ошибка при создании заказа: {e}")
            raise
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
            raise
        finally:
            print(f"🏁 Обработка создания заказа для товара '{product_name}' завершена")

    @property
    def total_quantity(self):
        return self.quantity

    def __str__(self):
        return f"Заказ: {self.product.name}, Количество: {self.quantity}, Итого: {self.total_value} руб."


class Sorting:
    """Класс сортировки продуктов по выбранной категории"""

    def __init__(self, categories: list[Category]):
        self.categories = categories
        self.need_find = input("Ввести категорию для сортировки продуктов: ")
        self.current_index = 0
        self.found_products = []

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


class Smartphone(Product):
    """Дочерний Класс для смартфонов"""

    def __init__(self, name, description, price, quantity, efficiency: float, model: str, memory: int, color: str):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self):
        return f"{self.name} ({self.model}), {self.price} руб. Остаток: {self.quantity} шт. Память: {self.memory}GB"


class LawnGrass(Product):
    """Дочерний Класс для газонной травы"""

    def __init__(self, name, description, price, quantity, country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт. Страна: {self.country}"


class ZeroQuantityError(Exception):
    """Исключение для товаров с нулевым количеством"""

    def __init__(self, product_name: str, operation: str):
        self.product_name = product_name
        self.operation = operation
        super().__init__(f"Товар '{product_name}' не может быть {operation}: количество равно нулю")


if __name__ == "__main__":
    try:
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
                    price=product_data["price"],
                    quantity=product_data["quantity"],
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
            products_objects = categories[0].get_products_objects()
            if products_objects:
                product = products_objects[0]
                print(f"Исходная цена: {product.price}")

                product.price = 150.0
                print(f"После валидного изменения: {product.price}")

                product.price = -50.0
                print(f"После невалидного изменения: {product.price}")

    except Exception as e:
        print(f"Ошибка: {e}")