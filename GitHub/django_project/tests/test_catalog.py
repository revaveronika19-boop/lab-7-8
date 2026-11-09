import pytest
from django.urls import reverse
from django.db.models import Count
from catalog.models import Category,Item,Tag,ItemDetail
@pytest.mark.django_db
def test_model_str(item):assert str(item)=='Тестовий запис'
@pytest.mark.django_db
def test_relationship(item):assert item.category.items.count()==1
@pytest.mark.django_db
def test_m2m(item):
 tag=Tag.objects.create(name='Новинка',slug='new');item.tags.add(tag);assert item.tags.count()==1
@pytest.mark.django_db
def test_one_to_one(item):
 detail=ItemDetail.objects.create(item=item,identifier='CODE-1');assert item.detail==detail
@pytest.mark.django_db
def test_get(client):assert client.get(reverse('home')).status_code==200
@pytest.mark.django_db
def test_api(client,item):assert client.get(reverse('api_items')).json()['items'][0]['title']==item.title
@pytest.mark.django_db
@pytest.mark.parametrize('term,expected',[('Тест',1),('Немає',0)])
def test_search(client,item,term,expected):
 response=client.get(reverse('items'),{'q':term});assert response.context['count']==expected
@pytest.mark.django_db
def test_protect(category,item):
 from django.db.models.deletion import ProtectedError
 with pytest.raises(ProtectedError):category.delete()
@pytest.mark.django_db
def test_feedback_invalid(client):
 response=client.post(reverse('feedback'),{'name':'Іра','email':'ira@example.com','category':'idea','message':'два слова'})
 assert 'message' in response.context['form'].errors
