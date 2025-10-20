from src.utils import load_transactions


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

    def __init__(self, name: str, description: str, products: list = None):
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

    @property
    def product_count(self):
        """Возвращает количество продуктов в категории"""
        return len(self.__products)

    def __str__(self):
        return f"Категория: {self.name}, продуктов: {self.product_count}"


if __name__ == "__main__":
    # Загружаем данные из JSON
    result = load_transactions("products.json")
    categories = []
    for category_data in result:

        category_products = []
        for product_data in category_data["products"]:
            product = Product(
                name=product_data["name"],
                description=product_data["description"],
                quantity=product_data["quantity"],
                price=product_data["price"]
            )
            category_products.append(product)

        # Создаем категорию с объектами Product
        category = Category(
            name=category_data["name"],
            description=category_data["description"],
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

    print(f"\n=== ОБЩАЯ СТАТИСТИКА ===")
    print(f"Всего категорий: {Category.total_categories}")
    print(f"Всего продуктов: {Category.total_products}")

    # Тестируем добавление нового продукта
    print(f"\n=== ТЕСТ ДОБАВЛЕНИЯ ПРОДУКТА ===")
    if categories:
        new_product = Product('Новый телевизор', "Тестовый продукт", 50000, 3)
        categories[0].add_product(new_product)  # Добавляем в первую категорию
        print(f"После добавления продукта в категорию '{categories[0].name}':")
        print(f"Количество продуктов: {categories[0].product_count}")
        print("Обновленный список продуктов:")
        for product_info in categories[0].products:
            print(f"  - {product_info}")
