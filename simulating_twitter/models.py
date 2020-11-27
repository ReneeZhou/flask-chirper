from datetime import datetime
from simulating_twitter import db, login_manager
from flask_login import UserMixin

# this func reloads user from the user id stored in the session
# use the decorator so the extension knows to get the user by id
# the extension expects 4 attributes from our models - is_authenticated, is_active, is_anonymous, get_id
# because these are so common, the extension has handled it by creating a class for us to inherit - UserMixin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    account_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    handle = db.Column(db.String(20), nullable = False, unique = True)  # handle
    name = db.Column(db.String(50), nullable = False)                   # profile name
    email = db.Column(db.String(120), nullable = False, unique = True)
    # dob = db.Column(db.Date, nullable = False)
    # dob_y = db.Column(db.Date, nullable = False)
    # dob_m = db.Column(db.Date, nullable = False)
    # dob_d = db.Column(db.Date, nullable = False)
    password = db.Column(db.String(60), nullable = False)

    profile_image = db.Column(db.String(20), nullable = False, default = 'default_profile.png')
    background_image = db.Column(db.String(20), nullable = False, default = '')  # db will default Null because nullable
    bio = db.Column(db.String(160), nullable = False, default = '')              # give it '' so it can render consistently in templates
    location = db.Column(db.String(30), nullable = False, default = '')
    website = db.Column(db.String(100), nullable = False, default = '')

    posts = db.relationship('Post', backref = 'author', lazy = True) 
    # referring to Post class

    def __repr__(self):
        return f'User("{self.name}", "{self.email}", "{self.handle}")'
     


class Post(db.Model):
    # id = db.Column(db.Integer, primary_key = True)
    # title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    post_id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
    # referring to user table and id col

    def __repr__(self):
        return f'Post("{self.user_id}", "{self.post_id}", "{self.date_posted}", f"{self.content}")'