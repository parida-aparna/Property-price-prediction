from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    mobile = db.Column(db.String(10), unique=False, nullable=False)
    aadhaar = db.Column(db.String(12), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.Boolean(), default=False, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Float, nullable= False)
    floors = db.Column(db.Integer, nullable= False)
    sqft_living = db.Column(db.Float, nullable= False)
    sqft_lot = db.Column(db.Float, nullable= False)
    sqft_basement = db.Column(db.Float, nullable= False)
    sqft_above = db.Column(db.Float, nullable= False)
    waterfront = db.Column(db.Integer, nullable= False)
    view = db.Column(db.Integer, nullable= False)
    condition = db.Column(db.Integer, nullable= False)
    grade = db.Column(db.Integer, nullable= False)
    yr_built = db.Column(db.Integer, nullable= False)
    yr_renovated = db.Column(db.Integer, nullable= False)
    zipcode = db.Column(db.Integer, nullable= False)
    price = db.Column(db.Float, nullable= False)
    docs = db.Column(db.String(20), nullable=False, default='random.pdf')
    verified = db.Column(db.String(1),nullable=False, default='N')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

