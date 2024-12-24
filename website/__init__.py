import os
import sys
from os import path
from flask import Flask

from flask import session
from flask_sqlalchemy import SQLAlchemy 		
from flask_login import LoginManager



#sys.path.append('../Website2')

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
	basedir = os.path.abspath(os.path.dirname(__file__))
	basedir1 = basedir[0:-8]

	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'jhsajdhjasjdj'

	
	app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir1, 'instance/database.db')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
	db.init_app(app)

	
	



	from .admin import admin
	from .views import views
	from .auth import auth
	

	
	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')
	app.register_blueprint(admin, url_prefix='/')

	from .models import User, Note

	create_database(app)
	
	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))

	return app 

    
#def create_database():
#	if not path.exists('website' + DB_NAME):
#		db.create_all()
#		print('Created Database!')


def create_database(app):
	with app.app_context():
		db.create_all()

	return app

