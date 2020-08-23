from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField, TextAreaField, FloatField, RadioField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange,Regexp,required
from flaskblog.models import User

regex1='^[0-9]{10}$'
regex2='^[0-9]{12}$'
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    mobile = StringField('mobile', validators=[DataRequired(), Length(min=10, max=10), Regexp(regex1, flags=0, message=None)])
    aadhaar = StringField('aadhaar', validators=[DataRequired(), Length(min=12, max=12), Regexp(regex2, flags=0, message=None)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    user_type = BooleanField('Do you want to login as a seller?')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_mobile(self, mobile):
        if len(mobile.data) > 10 and len(mobile.data)<10:
            raise ValidationError('Invalid mobile number.')

    def validate_aadhaar(self, aadhaar):
        if len(aadhaar.data) > 12 and len(aadhaar.data)<12:
            raise ValidationError('Invalid aadhaar number.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    Buyer = BooleanField('Buyer')
    user_type = BooleanField('Do you want to login as a seller?')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    mobile = StringField('mobile', validators=[DataRequired(), Length(min=10, max=10), Regexp(regex1, flags=0, message=None)])
    aadhaar = StringField('aadhaar', validators=[DataRequired(), Length(min=12, max=12), Regexp(regex2, flags=0, message=None)])
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data!=current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
         if email.data!=current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    bedrooms = IntegerField('Bedrooms')
    bathrooms = FloatField('Bathrooms' )
    floors = IntegerField('Floors' )
    sqft_living = FloatField('Sqft_Living' )
    sqft_lot = FloatField('Sqft_Lot' )
    sqft_above = FloatField('Sqft_Above' )
    sqft_basement = FloatField('Sqft_Basement' )
    waterfront = IntegerField('Waterfront')
    view = IntegerField('View' )
    condition = IntegerField('Condition' )
    grade = IntegerField('Grade' )
    yr_built = IntegerField('Year Built',validators=[DataRequired()] )
    yr_renovated = IntegerField('Year Renovated' )
    zipcode = IntegerField('Zipcode',validators=[DataRequired()] )
    price = FloatField('Price',validators=[DataRequired()])
    docs = FileField('Upload single PDF of required documents ', validators = [FileAllowed(['pdf'])])
    verified = HiddenField()
    submit = SubmitField('Post')


class IndexForm(FlaskForm):
    date = IntegerField('Date',validators=[DataRequired()])
    age = IntegerField('Age')
    distance = FloatField('Distance')
    stores = IntegerField('Stores')
    latitude = FloatField('Latitude',validators=[DataRequired()])
    longitude = FloatField('Longitude',validators=[DataRequired()])
    submit = SubmitField('Submit')


class BuyForm(FlaskForm):
    income = FloatField('Annual Income',
                           validators=[DataRequired()])
    loan = BooleanField('Whether loan required?')
    pan = FileField('Upload PAN card', validators = [FileAllowed(['jpg','png','txt','pdf'])])
    bill = FileField('Upload Electricity bill', validators = [FileAllowed(['jpg','png','txt','pdf'])])
    govt = BooleanField('Government Employee?')
    business = BooleanField('Business?')
    others = BooleanField('Others?')
    submit = SubmitField('Submit')