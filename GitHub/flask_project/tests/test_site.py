import pytest
from siteapp import db
from siteapp.models import Item,Category,Tag,ItemDetail
@pytest.mark.parametrize('path',['/','/items','/api/items','/api/stats'])
def test_pages(client,path):assert client.get(path).status_code==200
def test_create(client):
 response=client.post('/api/items',json={'title':'Новий','category_id':1,'price':25})
 assert response.status_code==201
def test_invalid(client):assert client.post('/api/items',json={'title':''}).status_code==400
def test_update(client):assert client.patch('/api/items/1',json={'title':'Оновлено'}).json['title']=='Оновлено'
def test_delete(client):assert client.delete('/api/items/1').status_code==204
def test_relations(app):
 with app.app_context():
  item=db.session.get(Item,1);tag=Tag(name='Важливо',slug='important');item.tags.append(tag)
  item.detail=ItemDetail(identifier='ID-1');db.session.commit()
  assert len(item.tags)==1 and item.detail.identifier=='ID-1'
def test_rollback(app):
 with app.app_context():
  before=Item.query.count();db.session.add(Item(title='Без категорії',category_id=999))
  from sqlalchemy.exc import IntegrityError
  with pytest.raises(IntegrityError):db.session.commit()
  db.session.rollback();assert Item.query.count()==before
