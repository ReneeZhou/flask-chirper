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
login_manager.login_view = 'login'

# customize message category
# login_manager.login_message_category ='info' 

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# initialize the extension with the config set
mail = Mail(app)
from simulating_twitter import routes