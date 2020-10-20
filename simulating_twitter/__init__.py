from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# instance_relative_config allows separation of private info
app = Flask(__name__, instance_relative_config = True)


# default value during development
# this will loag instance/config.py
app.config.from_pyfile('config.py')
# app.config.from_object('config') 


# overridden if this file exists in the instance folder



from simulating_twitter import routes