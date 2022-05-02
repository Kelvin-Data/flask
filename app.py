from fileinput import filename
import profile
from flask import Flask, redirect, render_template, flash, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from datetime import date
from webforms import  LoginForm, NameForm, PasswordForm, PostForm, SearchForm, UserForm
from flask_login import login_user, LoginManager, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
import uuid as uuid
import os

# Create a Flask Instance
app = Flask(__name__) # help flask find the directory & file

# Add a CKeditor
ckeditor = CKEditor(app)

# Add Old Database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_2.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://shqgzimtomlwwg:505ec34bd738b4015be1d486a58e24c7dd16d58ab0edb7338072066fb1472b40@ec2-52-5-110-35.compute-1.amazonaws.com:5432/ddtpdbksl1jcvk'

# Secret key!
app.config['SECRET_KEY'] = 'my super secret key that no one is supposed to know'

UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize The Database
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Add Post Page 
@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        poster = current_user.id  # 28
        post = Posts(
            title=form.title.data,
            content=form.content.data,
            #author=form.author.data,
            poster_id = poster,
            slug=form.slug.data,
            )
        form.title.data = ''
        form.content.data = ''
        #form.author.data = ''
        form.slug.data = ''

        # Add post data to database
        db.session.add(post)
        db.session.commit()

        # Return a message 
        flash("Blog Post Submitted Successfully!")

    # Redirect to the webpage
    return render_template('add_post3.html', form=form)


@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm() # refer to class userform
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hashing the password
            hashed_pw = generate_password_hash(form.password_hash.data, 'sha256')

            user = Users(
                username=form.username.data,
                name=form.name.data, 
                email=form.email.data,
                favourite_color=form.favourite_color.data,
                password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.favourite_color.data = ''
        form.password_hash.data = ''

        flash("User Added Successfully!")
    
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html',
            form=form,
            name=name,
            our_users=our_users)

# Create an admin page
@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 1:
        return render_template('admin.html')
    else: 
       flash("Sorry you must be an Admin in order to access the admin page!")
       return redirect(url_for('dashboard'))

# Pass stuff to nevbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form) # dictionery

# Create dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favourite_color = request.form['favourite_color']
        name_to_update.username = request.form['username']
        name_to_update.about_author = request.form['about_author']
        name_to_update.profile_pic = request.files['profile_pic']

        # Grab image name
        pic_filename = secure_filename(name_to_update.profile_pic.filename)
        #set a uuid
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        # Save the image
        saver = request.files['profile_pic']
        
        # Change it to a string to save to db
        name_to_update.profile_pic = pic_name
        try:
            db.session.commit()
            saver.save(os.path.join(app.config['UPLOAD_FOLDER']), pic_name)
            flash('User Updated Successfully!')
            return render_template('dashboard.html',
                form = form,
                name_to_update = name_to_update,
                id=id)

        except:
            flash('Error! Look like there was a problem...try again!')
            return render_template('dashboard.html',
                form = form,
                name_to_update = name_to_update)   
    else:
        return render_template('dashboard.html',
            form = form,
            name_to_update = name_to_update,
            id=id)
        return render_template('dashboard.html')

# Define delete 
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm() 

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User Deleted Successfully!')

        our_users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html',
            form=form,
            name=name,
            our_users=our_users)

    except:
        flash('Whoops! There was a problem deleting user')
        return render_template('add_user.html',
            form=form,
            name=name,
            our_users=our_users)

@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster.id:

        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            
            # Return a message
            flash('Blog Post Was Deleted!')

            # Grab all the posts from the database
            posts = Posts.query.order_by(Posts.date_posted) # Model is Posts on above
            return render_template('posts.html', posts=posts)

        except:
            # Return an error message
            flash('Woop, there is a problem to delete the post, please try again!')
            posts = Posts.query.order_by(Posts.date_posted) # Model is Posts on above
            return render_template('posts.html', posts=posts)

    else:
        # Return a message
        flash("You Aren't Authorized To Delete That Post")
        posts = Posts.query.order_by(Posts.date_posted) # Model is Posts on above
        return render_template('posts.html', posts=posts)

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
       # post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data

        # Uppdate to the database
        db.session.add(post)
        db.session.commit()

        # Return a message 
        flash("Blog Post Updated Successfully!")
        return redirect(url_for('post', id=post.id))

    if current_user.id == post.poster_id:
        form.title.data = post.title
        # form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('edit_post.html', form=form)
    else: 
        flash("You Are Not Authorised To Edit This Post")
        posts = Posts.query.order_by(Posts.date_posted) # Model is Posts on above
        return render_template('posts.html', posts=posts)

# Json stuff
@app.route('/date')
def get_current_date():
    favourite_pizza = {
        "John": "Pepperoni",
        "Mary": "Cheese",
        "Tim": "Mushroom"
    } 
    return favourite_pizza
   # return {"Date": date.today()}

# Create a route decorator
@app.route('/') # url www.about.html

def index():
    first_name = 'John'
     # stuff = 'This is <strong>Bold</strong> Text!' # for the striptags
    stuff = 'This is bold Text!'  # for the title
    flash("Welcome To Our Website!") 

    favourite_pizza = ['Pepperoni', 'Cheese', 'Mushroom', 41]
    return render_template('index.html', 
                first_name=first_name,
                stuff=stuff,
                favourite_pizza=favourite_pizza)

# Flask login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # Check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("You have logined!!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password - Try Again!")
        else:
            flash("That User Doesn't Exist! Please Try Again...")

    return render_template('login.html', form=form)

# Create logout page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!, Thanks..")
    return redirect(url_for('login'))

# Create Name Page
@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    form = NameForm() # Refer classes
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Has Been Submitted")  # Flash message is here!

    return render_template('name.html',
        name = name,
        form = form)


@app.route('/posts')
def posts():
    # Grab all the posts from the database
    posts = Posts.query.order_by(Posts.date_posted) # Model is Posts on above
    return render_template('posts.html', posts=posts)

@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

# Create a custom error pages
# Invalid URL pages
@app.errorhandler(404)

def page_not_found(e):
    return render_template('404.html'),404

# Internal server error
@app.errorhandler(500)

def page_not_found(e):
    return render_template('505.html'),500


# Create Test Page
@app.route('/test_pw', methods=['GET','POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm() # Refer classes

    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data

        # Clear the form
        form.email.data = ''
        form.password_hash.data = ''

        # Lookup user by the email address
        pw_to_check = Users.query.filter_by(email=email).first # retrurn the first result

        # Check the hashed password
        # passed = check_password_hash(pw_to_check.password_hash, password)

    return render_template("test_pw.html",
        email = email,
        password = password,
        pw_to_check = pw_to_check,
        passed = passed,
        form = form)

# Create search function
@app.route('/search', methods=["POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        posts = Posts.query
        # Get data from submitted form
        post.searched = form.searched.data
        # Query the database
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()
        return render_template("search2.html", 
            form=form,
            searched=post.searched,
            posts=posts)

# Update The Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])  # int is integer
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favourite_color = request.form['favourite_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()

            flash('User Updated Successfully!')
            return render_template('update.html',
                form = form,
                name_to_update = name_to_update,
                id=id)

        except:
            flash('Error! Look like there was a problem...try again!')
            return render_template('update.html',
                form = form,
                name_to_update = name_to_update)   
    else:
        return render_template('update.html',
            form = form,
            name_to_update = name_to_update,
            id=id)


# localhost:5000/user/John or http://127.0.0.1:5000  # the dyanmic name
@app.route('/user/<name>')

def user(name):
    return render_template('user.html', user_name=name) # first name from user.html 
                                                        # second name from definition

# Create a blog post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
   #author = db.Column(db.String(255)) # 28
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    # Foreign key to link users(refer to primary key of user)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id')) # 28
    # query the databaseflask db upgrade 

# Create Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary key is an id
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False) # nullable mean can not be blank                         
    email = db.Column(db.String(120), nullable=False, unique=True) 
    # unique mean we don't want 2 the repeated email address
    favourite_color = db.Column(db.String(120))
    about_author = db.Column(db.Text(), nullable=True)  # db.Text(500)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    profile_pic = db.Column(db.String(), nullable=True)  # Not save the picture but save the name
    # User can have many posts
    posts = db.relationship('Posts', backref='poster') # 28

    # Do some password stuff!   # 28
    password_hash = db.Column(db.String(128))

    @ property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name


# Powershell
# $env:FLASK_APP = "app.py" 
# $env:FLASK_ENV = "development"
# flask run

# heroku -v (version)
# pip install gunicorn
# pip install psycopg2
# pip freeze > requirements.txt
# echo web: gunicorn app:app > Procfile
# heroku login
# heroku create flasker112
# ==> https://flasker112.herokuapp.com/ | https://git.heroku.com/flasker112.git
# heroku addons:create heroku-postgresql:hobby-dev --app flasker112
# ==> Created postgresql-vertical-43113 as DATABASE_URL
# heroku config --app flasker112
# ==> postgres://shqgzimtomlwwg:505ec34bd738b4015be1d486a58e24c7dd16d58ab0edb7338072066fb1472b40@ec2-52-5-110-35.compute-1.amazonaws.com:5432/ddtpdbksl1jcvk
# git init
# git add .
# git commit -am 'geat'
# git push heroku 
# heroku git:remote -a flasker112
# support ticket : a7b5a1c6-808f-89b9-9518-384b5d648e41 
# https://help.heroku.com/sharing/20bc3267-fd1b-42b4-b97f-3a90338bedd5
# https://help.heroku.com/sharing/5ff5b94c-95dc-40bd-b83f-9d46d979bfed

# heroku run python
# >>> from app import db
# >>> db.create_all()
# >>> exit()