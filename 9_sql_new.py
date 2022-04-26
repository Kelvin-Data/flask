from turtle import clear
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a Flask Instance
app = Flask(__name__) # help flask find the directory & file

# Add New Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Bhlohass*76@localhost/our_users'

# Secret key!
app.config['SECRET_KEY'] = 'my super secret key that no one is supposed to know'

# Initialize The Database
db = SQLAlchemy(app)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary key is an id
    name = db.Column(db.String(200), nullable=False) # nullable mean can not be blank                         
    email = db.Column(db.String(120), nullable=False, 
            unique=True) # unique mean we don't want 2 the repeated email address
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name

# Create form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit =SubmitField("Submit")

# Create form class
class NameForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit =SubmitField("Submit")

@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm() # refer to class userform
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''

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


### MySql installer for window ###
# https://dev.mysql.com/downloads/installer/

### MySql installer for VS Code ###
# https://dev.mysql.com/downloads/windows/visualstudio/

### MySQL password ###
# Bhlohass*76

### Change password in workbench ###
## ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Bhlohass*76';
## click the lighning icon

# python
# from sql_new import db
# db.create_all()
# exit()


# Powershell
# $env:FLASK_APP = "9_sql_new.py" 
# $env:FLASK_ENV = "development"
# flask run