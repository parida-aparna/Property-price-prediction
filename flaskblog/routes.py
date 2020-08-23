import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort,jsonify
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, BuyForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import numpy as np
import pickle


@app.route("/")
def entry():
    return render_template('entry.html')
    
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        user = User(username=form.username.data, email=form.email.data, mobile=form.mobile.data, aadhaar=form.aadhaar.data, password=hashed_password,user_type = form.user_type.data)
       
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)

    output_size = (125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        current_user.mobile=form.mobile.data
        current_user.aadhaar=form.aadhaar.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.mobile.data = current_user.mobile
        form.aadhaar.data = current_user.aadhaar
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

def save_file(form_file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    file_fn = random_hex + f_ext
    file_path = os.path.join(app.root_path,'static/documents',file_fn)

    output_size = (125,125)
    i=Image.open(form_file)
    i.thumbnail(output_size)
    i.save(file_path)

    return file_fn


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, bedrooms=form.bedrooms.data, bathrooms=form.bathrooms.data, floors=form.floors.data, sqft_living=form.sqft_living.data, sqft_lot=form.sqft_lot.data, sqft_above=form.sqft_above.data, sqft_basement=form.sqft_basement.data, condition=form.condition.data, grade=form.grade.data, waterfront=form.waterfront.data, view=form.view.data, yr_built=form.yr_built.data, yr_renovated=form.yr_renovated.data, zipcode=form.zipcode.data, price=form.price.data, verified='N', author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been submitted.Wait till verification!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.docs.data:
            docs_file = save_file(form.docs.data)
            post.docs = docs_file
        post.title = form.title.data
        post.bedrooms = form.bedrooms.data
        post.bathrooms = form.bathrooms.data
        post.floors = form.floors.data
        post.sqft_living = form.sqft_living.data
        post.sqft_lot = form.sqft_lot.data
        post.sqft_above = form.sqft_above.data
        post.sqft_basement = form.sqft_basement.data
        post.condition = form.condition.data
        post.grade = form.grade.data
        post.waterfront = form.waterfront.data
        post.view = form.view.data
        post.yr_built = form.yr_built.data
        post.yr_renovated = form.yr_renovated.data
        post.zipcode = form.zipcode.data
        post.price = form.price.data
        docs=url_for('static', filename='documents/' + post.docs)

        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.bedrooms.data = post.bedrooms
        form.bathrooms.data=post.bathrooms
        form.floors.data=post.floors 
        form.sqft_living.data=post.sqft_living
        form.sqft_lot.data= post.sqft_lot 
        form.sqft_above.data= post.sqft_above
        form.sqft_basement.data= post.sqft_basement
        form.condition.data=post.condition 
        form.grade.data= post.grade
        form.waterfront.data= post.waterfront
        form.view.data=post.view
        form.yr_built.data= post.yr_built  
        form.yr_renovated.data=post.yr_renovated
        form.zipcode.data=post.zipcode  
       
        form.price.data = post.price
        docs = url_for('static', filename='documents/' + post.docs)

    return render_template('update_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@app.route("/post/<int:post_id>/choose", methods=['GET', 'POST'])
@login_required
def choose_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('choose_post.html', title='Chosen Post', post=post)


@app.route("/post/choose/buy_ppty", methods=['GET', 'POST'])
@login_required
def buy_ppty():
    form = BuyForm()
    if form.validate_on_submit():
        flash('Your details have been submitted. The seller will contact you soon', 'success')
        return redirect(url_for('home'))
    return render_template('buy_ppty.html', title='Fill form',
                           form=form)


# ML 

model = pickle.load(open('lr_model_flask.pkl', 'rb'))

@app.route("/prediction")
@login_required
def prediction():
    return render_template('index.html', title='Prediction')


@app.route('/predictprice',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    predicting = model.predict(final_features)

    output = round(predicting[0], 2)

    return render_template('index.html', prediction_text='House price should be $ {}'.format(output))



class MyModelView(ModelView):
    def is_accesssible(self):
        if current_user.is_authenticated:
            return current_user.email == 'admin@email.com' and bcrypt.check_password_hash(current_user.password, '12345')

       

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.email == 'admin@email.com' and bcrypt.check_password_hash(current_user.password, '12345')

        


admin=Admin(app, index_view = MyAdminIndexView())

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Post, db.session))