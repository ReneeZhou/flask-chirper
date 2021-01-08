from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from simulating_twitter import db, login_manager    # so we can use app's secret key in the serializer


# this func reloads user from the user id stored in the session
# use the decorator so the extension knows to get the user by id
# the extension expects 4 attributes from our models - is_authenticated, is_active, is_anonymous, get_id
# because these are so common, the extension has handled it by creating a class for us to inherit - UserMixin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# don't need @declared_attr as it doesn't involve ForeignKey
class TimestampMixin:    # causing error if inherit from db.Model here
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)




# not declaring this table as a model as this is an auxiliary table
# which has no data other than foreign keys
follower = db.Table(
    'follower', 
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('following_id', db.Integer, db.ForeignKey('user.id'))
    )



class User(db.Model, UserMixin, TimestampMixin):
    # account_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    created_at_ip = db.Column(db.String, nullable = False)
    id = db.Column(db.Integer, primary_key = True)
    handle = db.Column(db.String(20), nullable = False, unique = True)  # handle
    name = db.Column(db.String(50), nullable = False)                   # profile name
    email = db.Column(db.String(120), nullable = False, unique = True)
    phone = db.Column(db.String(20), nullable = True, unique = True)
    birthdate = db.Column(db.Date, nullable = False)
    # dob_y = db.Column(db.Date, nullable = False)
    # dob_m = db.Column(db.Date, nullable = False)
    # dob_d = db.Column(db.Date, nullable = False)
    password = db.Column(db.String(60), nullable = False)

    profile_image = db.Column(db.String(20), nullable = False, default = 'default_profile.png')
    background_image = db.Column(db.String(20), nullable = False, default = '')  # db will default Null because nullable
    bio = db.Column(db.String(160), nullable = False, default = '')              # give it '' so it can render consistently in templates
    location = db.Column(db.String(30), nullable = False, default = '')
    website = db.Column(db.String(100), nullable = False, default = '')

    posts = db.relationship('Post', backref = 'author', lazy = True)             # same as lazy = 'select' 
    # referring to Post class


    following = db.relationship('User', secondary = follower, 
        primaryjoin = (follower.c.follower_id == id),             # this user's following people
        secondaryjoin = (follower.c.following_id == id),          # this user's followers
        backref = db.backref('follower', lazy = 'dynamic'), 
        lazy = 'dynamic')

    
    message_sent = db.relationship('Message', backref = 'sender', lazy = 'dynamic', foreign_keys = 'Message.sender_id')
    message_received = db.relationship('Message', backref = 'recipient', lazy = 'dynamic', foreign_keys = 'Message.recipient_id')
    last_read_message_at = db.Column(db.DateTime, nullable = True)


    # return numbers of unread messages
    def new_messages(self):
        last_read_time = self.last_read_message_at or datetime(1990, 1, 1)
        return Message.query.filter_by(recipient_id = self.id).filter(
            Message.created_at > last_read_time).count()
            # same as Message.query.filter_by(recipient = self).filter(
                # Message.created_at > last_read_time).count()
            # can either filter_by a column value
            # or filter_by the entire matching obj to that 'relationship'
            # 'relationship' is not a column


    def is_following(self, user):
        return self.following.filter(follower.c.following_id == user.id).count() > 0
        # left side foreign key set to self, right side set to user?????? 
        # ok, essentially in the 'following' column, leave only where the following_id is this 'other' user's id
        # and the self id is the matching follower_id, as a follower
        # as we're asking if this row of entry of this user, is following this external user (other row, other entry)

        # this syntax is probably because according to primaryjoin
        # if switching primaryjoin & secondaryjoin, it might be different?????
        # again, everything comes back to model tables being defined that the left table 'follows' the right table
        # hence, primaryjoin performs the follower user joining the association table

        # filter_by() can only check for equality of a certain value
        # whereas filter() is lower level, can handle more complicated filter conditions
        # c is an SQLAlchemy attribute for tables, where column and subattributes of c

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)


    def following_post(self):
        following_post = Post.query.join(follower, (follower.c.following_id == Post.user_id)).filter(
            follower.c.follower_id == self.id)
        own_post = Post.query.filter_by(user_id = self.id)
        return following_post.union(own_post).order_by(Post.created_at.desc())
        
        # Post table join the follower table, with the condition of (...)
        # the follower table's following_id col should be the sane as post's user_id 
        # as in post being written by people we're following
        # now only people we follow is left in the table, with all their posts
        # [ actually not even, we don't have a specific user here, so it's the entire Post table]
        # [ so we can think about filtering first actually, instead of joining ]
        # we have all cols & follower table's cols
        # so we're filtering by 


    # method to create token for serializer
    def get_reset_token(self, expires_sec = 180):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)    # serializer obj
        return s.dumps({'user_id': self.id}).decode('utf-8')  
        # return the token created with this serializer
        # that contains the payload of the current user's id


    # method to verify a token
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        # exception could happen when we try to load the token
        # when the token is invalid, time expires or something else
        try: 
            user_id = s.loads(token)['user_id']    # 'user_id' comes from the payload we load in
        except:
            return None                            # this will exit us from this method
        return User.query.get(user_id)             # if we didn't hit the earlier return statement, we will query that user
    # this method never used this class's instance (the self variable) -> static method


    def __repr__(self):
        return f'User("{self.name}", "{self.email}", "{self.handle}")'
     


class Post(db.Model, TimestampMixin):
    __searchable__ = ['body']

    # id = db.Column(db.Integer, primary_key = True)
    # title = db.Column(db.String(100), nullable = False)
    # date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    post_id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
    # referring to user table and id col

    def __repr__(self):
        return f'Post("{self.user_id}", "{self.post_id}", "{self.created_at}", f"{self.content}")'



class Message(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key = True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    body = db.Column(db.String(500), nullable = False)
    read_at = db.Column(db.DateTime, nullable = True)

    def repr(self):
        return f'<Message {self.body}>'