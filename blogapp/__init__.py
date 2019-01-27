from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from blogapp.config import Config as config_class
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object(config_class)


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
mail = Mail(app)


from blogapp.views.index import index
app.register_blueprint(index)

from blogapp.views.auth import auth
app.register_blueprint(auth)

from blogapp.views.posts import posts
app.register_blueprint(posts)

from blogapp.views.errors import errors
app.register_blueprint(errors)

from blogapp.views.comments import comments
app.register_blueprint(comments)
