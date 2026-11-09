import pytest
from siteapp import create_app,db
from siteapp.models import Category,Item
@pytest.fixture
def app(tmp_path):
 app=create_app({'TESTING':True,'WTF_CSRF_ENABLED':False,'SQLALCHEMY_DATABASE_URI':'sqlite:///'+str(tmp_path/'test.sqlite3')})
 with app.app_context():
  db.create_all();c=Category(name='Тест',code='test');db.session.add(c);db.session.commit();db.session.add(Item(title='Перший запис',category=c,price=30));db.session.commit()
  yield app
  db.session.remove();db.drop_all()
@pytest.fixture
def client(app):return app.test_client()
