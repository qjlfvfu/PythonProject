import pytest

from src.classification import Category, Product


@pytest.fixture
def list_category():
    """Фикстура возвращает Список продуктов в категории"""
    return Category("Мясо", [" Тофик", "Бобик", "Вася"], "Грустно но вкусно")


@pytest.fixture
def sausage():
    return Product("Колбаса", "Краковская колбаса прямо из под собаки", 25, 1.40)
