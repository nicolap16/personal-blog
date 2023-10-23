from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '3a30c16c466f3b6c90b747a2b8beeb8817359a586931867b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c21016073:{}@csmysql.cs.cf.ac.uk:3306/c21016073_flaskblog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from blog import routes

from flask_admin import Admin
from blog.views import AdminView
from blog.models import User, Post, Comment
admin = Admin(app,name='Admin panel',template_mode='bootstrap3')
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Post, db.session))
admin.add_view(AdminView(Comment, db.session))
