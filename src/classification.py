import json

from src.utils import load_transactions


class Product:
    name = str
    description = str
    price = float
    quantity = int
    """Класс описания свойств продукта"""

    def __init__(self, name, description, quantity, price):
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
            name=product_data['name'],
            description=product_data['description'],
            quantity=product_data['quantity'],
            price=product_data['price']
        )


class Category:
    """Класс категорий продукта"""

    products = []
    total_categories = 0
    total_products = 0

    def __init__(self, name, products, description):
        self.name = name
        self.__products = products  # Сделали приватным
        self.description = description

        # Автоматически обновляем атрибуты класса при создании объекта
        Category.total_categories += 1
        Category.total_products += len(products)

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


if __name__ == "__main__":
    result = load_transactions("products.json")
    products = []
    for item in result:
        product = Product(
            name=item["name"], description=item["description"], quantity=item["quantity"], price=item["price"]
        )
        products.append(product)
        print(products)
        categories = []
        for category in result:
            product = Category(name=item["name"], description=item["description"], products=item["products"])
            print(categories)
