import pytest
from catalog.models import Category,Item
@pytest.fixture
def category(db):return Category.objects.create(name='Навчальна',code='study',description='Тест')
@pytest.fixture
def item(category):return Item.objects.create(title='Тестовий запис',category=category,price=120)
