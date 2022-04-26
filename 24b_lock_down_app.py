from flask import Flask, redirect, render_template, flash, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from wtforms.widgets import TextArea
from flask_login import login_user, LoginManager, login_required, logout_user, UserMixin, current_user

# Create a Flask Instance
app = Flask(__name__) # help flask find the directory & file

# Add Old Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_2.db'

# Secret key!
app.config['SECRET_KEY'] = 'my super secret key that no one is supposed to know'

# Initialize The Database
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Flask login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Create login form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Submit')

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

# Create dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

# Create a blog post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))

# Create posts form
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()], 
        widget=TextArea())
    author = StringField('Author', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        
        # Return a message
        flash('Blog Post Was Deleted!')
        posts = Posts.query.order_by(Posts.date_posted) # Model is Posts on above
        return render_template('posts.html', posts=posts)

    except:
        # Return an error message
        flash('Woop, there is a problem to delete the post, please try again!')
        posts = Posts.query.order_by(Posts.date_posted) # Model is Posts on above
        return render_template('posts.html', posts=posts)

@app.route('/posts')
def posts():
    # Grab all the posts from the database
    posts = Posts.query.order_by(Posts.date_posted) # Model is Posts on above
    return render_template('posts.html', posts=posts)

@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data

        # Uppdate to the database
        db.session.add(post)
        db.session.commit()

        # Return a message 
        flash("Blog Post Updated Successfully!")
        return redirect(url_for('post', id=post.id))

    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html', form=form)

# Add Post Page 
@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(
            title=form.title.data,
            content=form.content.data,
            author=form.author.data,
            slug=form.slug.data,
            )
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        # Add post data to database
        db.session.add(post)
        db.session.commit()

        # Return a message 
        flash("Blog Post Submitted Successfully!")

    # Redirect to the webpage
    return render_template('add_post2.html', form=form)

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

# Create Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary key is an id
    username = db.Column(db.String(20), nullable=False,
            unique=True)
    name = db.Column(db.String(200), nullable=False) # nullable mean can not be blank                         
    email = db.Column(db.String(120), nullable=False, 
            unique=True) # unique mean we don't want 2 the repeated email address
    favourite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Do some password stuff!
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

# Create form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favourite_color = StringField("Favourite Color")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo(
        'password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit =SubmitField("Submit")

# Update The Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])  # int is integer
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favourite_color = request.form['favourite_color']
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

# Create form class
class NameForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit =SubmitField("Submit")

# Create form class
class PasswordForm(FlaskForm):
    email = StringField("What's Your Email", validators=[DataRequired()])
    password_hash = PasswordField("What's Your Password", validators=[DataRequired()])
    submit =SubmitField("Submit")

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
        form.username.data = ''
        form.name.data = ''
        form.email.data = ''
        form.favourite_color.data = ''
        form.password_hash = ''

        flash("User Added Successfully!")
    our_users = Users.query.order_by(Users.date_added)

    return render_template('add_user.html',
            form=form,
            name=name,
            our_users=our_users)
                
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
    
# localhost:5000/user/John or http://127.0.0.1:5000  # the dyanmic name
@app.route('/user/<name>')

def user(name):
    return render_template('user.html', user_name=name) # first name from user.html 
                                                        # second name from definition

# Create a custom error pages
# Invalid URL pages
@app.errorhandler(404)

def page_not_found(e):
    return render_template('404.html'),404

# Internal server error
@app.errorhandler(500)

def page_not_found(e):
    return render_template('505.html'),500

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

# Powershell
# $env:FLASK_APP = "24b_lock_down_app.py" 
# $env:FLASK_ENV = "development"
# flask run

# Add login.html
# Add dashboard.html
