import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

# instance_relative_config allows separation of private info
app = Flask(__name__, instance_relative_config = True)


# default value during development
# this will loag instance/config.py
app.config.from_pyfile('config.py')
# app.config.from_object('config') 


# overridden if this file exists in the instance folder


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# telling the extension where the login route is located when login_required
login_manager.login_view = 'auth.login'

# customize message category
# login_manager.login_message_category ='info' 

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# initialize the extension with the config set
mail = Mail(app)


# from simulating_twitter import routes
# instead of importing routes registered with app (@app) like above
# we are importing blueprint instances and register them with our routes
from simulating_twitter.account.routes import account
from simulating_twitter.auth.routes import auth
from simulating_twitter.error.routes import error
from simulating_twitter.main.routes import main
from simulating_twitter.post.routes import post
from simulating_twitter.user.routes import user
from simulating_twitter.user_settings.routes import user_settings
from simulating_twitter.subdomain.routes import subdomain

app.register_blueprint(account)
app.register_blueprint(auth)
app.register_blueprint(error)
app.register_blueprint(main)
app.register_blueprint(post)
app.register_blueprint(user)
app.register_blueprint(user_settings)
app.register_blueprint(subdomain)