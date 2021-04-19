from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from simulating_twitter.config import Config


# create the extension outside of the create_app()
# but initialize them inside the func with the application
# so the extension object doesn't initially get bound to the application
# no application specific state is stored on the extension object
# one extension object can be used for multiple apps
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
# telling the extension where the login route is located when login_required
login_manager.login_view = 'auth.login'
# customize message category
# login_manager.login_message_category ='info' 
# initialize the extension with the config set
mail = Mail()


# create different instances of our app with different configs
def create_app(config_class = Config):

    # instance_relative_config allows separation of private info
    app = Flask(__name__, instance_relative_config = True)

    # default value during development
    # this will load instance/config.py
    # app.config.from_pyfile('config.py')           #### temporarily disabled for Heroku deployment


    # app.config.from_object('config') 
    # overridden if this file exists in the instance folder
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # from simulating_twitter import routes
    # instead of importing routes registered with app (@app) like above
    # we are importing blueprint instances and register them with our routes
    from simulating_twitter.account.routes import account
    from simulating_twitter.auth.routes import auth
    from simulating_twitter.error.handlers import error
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

    return app