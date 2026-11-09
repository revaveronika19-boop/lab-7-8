# ЛБ №7–8 — Каталог літературних подій

Студент: Рева Вероніка, група БІКСб2-25-4-0д.

## Django

```powershell
cd django_project
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations catalog
python manage.py migrate
python manage.py runserver
```

В іншому терміналі в каталозі django_project: `python -m pytest -v`.

## Flask

```powershell
cd flask_project
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
$env:FLASK_APP='app.py'
flask db init
flask db migrate -m 'initial'
flask db upgrade
flask run
```

У наступних запусках `flask db init` повторювати не треба. Для перевірки: `python -m pytest -v`.

Django: http://127.0.0.1:8000/; Flask: http://127.0.0.1:5000/.

**Важливо:** це навчальні проєкти; не розгортати публічно без автентифікації, production SECRET_KEY та перевірки доступу. Міграції, скриншоти та результати запуску треба отримати на власному ПК після встановлення залежностей.
