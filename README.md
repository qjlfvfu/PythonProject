# **📦 Product & Category Management System**

Система для управления продуктами и категориями с возможностью сортировки и анализа данных.

# 🚀 Возможности

## 🛍️ Управление продуктами

Создание и редактирование продуктов

Валидация цены (не может быть отрицательной или нулевой)

Строковое представление в формате: "Название, цена руб. Остаток: количество шт."

Сложение продуктов для расчета общей стоимости

## **📂 Управление категориями**

Создание категорий продуктов

Автоматический подсчет статистики

Строкое представление в формате: "Название категории, количество продуктов: X шт."

Расчет общей стоимости товаров в категории

## **🔍 Сортировка и поиск**

* Поиск продуктов по категориям
* 
* Итерация по найденным продуктам
* 
* Регистронезависимый поиск

## **🏗️ Структура проекта**

text
project/
├── src/
│   ├── classification.py  # Основные классы Product, Category, Sorting
│   └── utils.py          # Вспомогательные функции
├── tests/
│   └── test_classification.py  # Тесты
├── run_tests.py          # Запуск тестов
└── products.json         # Пример данных (опционально)

## **📋 Классы и методы**

### **🎯 Класс Product**

python
product = Product("iPhone", "Смартфон", 10, 1000.0)
Основные методы:

__init__(name, description, quantity, price) - конструктор

@property price - геттер цены

@price.setter - сеттер с валидацией

__add__(other) - сложение продуктов (возвращает общую стоимость)

__str__() - строковое представление

@classmethod new_product() - создание из словаря

### 📁 Класс Category

python
category = Category("Смартфоны", "Мобильные устройства", [product1, product2])
Основные методы:

__init__(name, description, products) - конструктор

add_product(product) - добавление продукта

@property products - список продуктов в текстовом формате

@property total_quantity - общее количество товаров

@property total_value - общая стоимость товаров

__str__() - строковое представление

get_products_objects() - получение объектов продуктов

@classmethod print_statistics() - вывод статистики

### 🔎 Класс Sorting
python
sorter = Sorting(categories_list)
Основные методы:

__init__(categories) - конструктор с запросом категории

__iter__(), __next__() - поддержка итерации

print_sorted_products() - вывод найденных продуктов

# **💻 Использование**
Базовое использование
python
from src.classification import Product, Category

## Создание продуктов
`product1 = Product("Телефон", "Смартфон", 5, 1000.0)
product2 = Product("Планшет", "Планшет", 3, 2000.0)`

## Создание категории
`category = Category("Электроника", "Техника", [product1, product2])`

### Вывод информации
`print(category)`
### Вывод: Электроника, количество продуктов: 8 шт.

for product_info in category.products:
    print(f"- {product_info}")
# Вывод:
# - Телефон, 1000.0 руб. Остаток: 5 шт.
# - Планшет, 2000.0 руб. Остаток: 3 шт.
Сложение продуктов
python
# Расчет общей стоимости
total = product1 + product2
print(f"Общая стоимость: {total} руб.")
# Вывод: Общая стоимость: 11000.0 руб.
# (5 * 1000 + 3 * 2000 = 5000 + 6000 = 11000)
Сортировка по категориям
python
from src.classification import Sorting

# Создание нескольких категорий
categories = [category_phones, category_laptops, category_tablets]

# Сортировка (запросит ввод категории)
sorter = Sorting(categories)

# Вариант 1: Итерация
for product in sorter:
    print(product)

# Вариант 2: Прямой вывод
sorter.print_sorted_products()
Загрузка из JSON
python
from src.utils import load_transactions

# Загрузка данных
data = load_transactions("products.json")

# Создание категорий и продуктов
`categories = []
for category_data in data:
    products = [
        Product(
            name=product_data["name"],
            description=product_data.get("description", ""),
            quantity=product_data["quantity"],
            price=product_data["price"]
        )
        for product_data in category_data["products"]
    ]
    category = Category(
        name=category_data["name"],
        description=category_data.get("description", ""),
        products=products
    )
    categories.append(category)`
# 🧪 Тестирование
Запуск всех тестов
bash
`_python run_tests.py_`
## Структура тестов
TestProductFeatures - тесты для класса Product

TestCategoryFeatures - тесты для класса Category

TestSortingFeatures - тесты для класса Sorting

TestIntegrationFeatures - интеграционные тесты

TestEdgeCases - тесты граничных случаев

## Пример теста
`python
def test_product_addition(self):
    product1 = Product("A", "Товар", 10, 100.0)
    product2 = Product("B", "Товар", 5, 200.0)
    result = product1 + product2  # 10*100 + 5*200 = 2000
    self.assertEqual(result, 2000.0)`
# 📊 Особенности реализации
### 🔒 Инкапсуляция
* Приватные атрибуты с двойным подчеркиванием
* 
* Геттеры и сеттеры для контроля доступа
* 
* Валидация данных при установке значений

### 🔄 Полиморфизм
* Переопределение магических методов (__str__, __add__, __iter__, __next__)
* 
* Единый интерфейс для разных типов операций

### 📈 Статистика
* Автоматический подсчет категорий и продуктов
* 
* Классовые атрибуты для хранения статистики

# **🛠️ Требования**
**Python 3.7+**

###### _Истинная Вера хоть в одного из богов_

Стандартные библиотеки (unittest для тестов)

##🎯 Пример данных (products.json)
`json
[
  {
    "name": "Смартфоны",
    "description": "Мобильные телефоны",
    "products": [
      {
        "name": "iPhone 15",
        "description": "Флагман Apple",
        "price": 999.0,
        "quantity": 10
      },
      {
        "name": "Samsung Galaxy",
        "description": "Флагман Samsung",
        "price": 899.0,
        "quantity": 15
      }
    ]
  }
]`
# 📝 Примечания
* Система автоматически обновляет статистику при создании объектов 
* 
* Все операции с ценами защищены валидацией
* 
* Поиск категорий регистронезависимый
* 
* Итератор Sorting можно использовать многократно

## 🏗️ Структура проекта

PythonProject/
├── src/
│ ├── classification.py # Основные классы Product, Category и Sorting
│ ├── main.py # Главный скрипт для демонстрации
│ └── utils/ # Утилиты для работы с файлами
├── tests/ # Тесты
│ ├── confest.py # Фикстуры проекта
│ └── test_classification.py
├── data/ # Данные (JSON файлы)
│ └── products.json
├── requirements.txt # Зависимости проекта
└── README.md # Этот файл
