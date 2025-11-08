from typing import Any
from abc import ABC,abstractmethod
from src.utils import load_transactions


class MixinInfo:
    """Миксин для логирования создания объектов"""

    def __init__(self, *args, **kwargs):
        """Инициализация с логированием создания объекта"""
        super().__init__(*args, **kwargs)
        print(f"{self.__class__.__name__}('{getattr(self, 'name', '')}', '{getattr(self, 'description', '')}',"
              f" {getattr(self, 'price', 0)}, {getattr(self, 'quantity', 0)})")


class BaseProduct(ABC,MixinInfo):
    """Абстрактный базовый класс для всех продуктов"""

    @abstractmethod
    def __init__(self, name: str, description: str, quantity: float, price: float):
        self.name = name
        self.description = description
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

    def __init__(self, name: str, description: str, quantity: float, price: float):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.__price = price
        super().__init__(name, description, quantity, price)

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
    def total_quantity(self)->int:
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

        # Автоматически обновляем атрибуты класса при создании объекта
        Category.category_count += 1
        Category.total_products += len(self.__products)

    def add_product(self, product):
        """Добавляет продукт в категорию"""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product")
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


class Order(BaseCounter):
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
        self.total_value = product.price * quantity
        self.name = f"Заказ {product.name}"
        super().__init__()

    @property
    def total_quantity(self):
        return self.quantity

    def __str__(self):
        return f"Заказ: {self.product.name}, ..."


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


class Smartphone(Product):
    """Дочерний Класс для смартфонов"""

    def __init__(self, name, description, quantity, price, efficiency: float, model: str, memory: int, color: str):
        super().__init__(name, description, quantity, price)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self):
        return f"{self.name} ({self.model}), {self.price} руб. Остаток: {self.quantity} шт. Память: {self.memory}GB"



class LawnGrass(Product):
    """Дочерний Класс для газонной травы"""

    def __init__(self, name, description, quantity, price, country: str, germination_period: str, color: str):
        super().__init__(name, description, quantity, price)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт. Страна: {self.country}"





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
