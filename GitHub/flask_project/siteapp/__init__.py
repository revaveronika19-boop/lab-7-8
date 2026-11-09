import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

db=SQLAlchemy();migrate=Migrate();csrf=CSRFProtect()
def create_app(test_config=None):
 app=Flask(__name__,template_folder='templates',static_folder='static')
 app.config.update(SECRET_KEY=os.environ.get('FLASK_SECRET_KEY','local-development-change-me'),SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL','sqlite:///catalog.sqlite3'),SQLALCHEMY_TRACK_MODIFICATIONS=False,THEME='Каталог літературних подій')
 if test_config:app.config.update(test_config)
 db.init_app(app);migrate.init_app(app,db);csrf.init_app(app)
 from .routes import bp
 app.register_blueprint(bp)
 return app
