from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

# Create a Flask Instance
app = Flask(__name__) # help flask find the directory & file

# Add Old Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_2.db'
# Secret key!
app.config['SECRET_KEY'] = 'my super secret key that no one is supposed to know'

# Initialize The Database
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary key is an id
    name = db.Column(db.String(200), nullable=False) # nullable mean can not be blank                         
    email = db.Column(db.String(120), nullable=False, 
            unique=True) # unique mean we don't want 2 the repeated email address
    favourite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name

# Create form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favourite_color = StringField("Favourite Color")
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
                name_to_update = name_to_update)

        except:
            flash('Error! Look like there was a problem...try again!')
            return render_template('update.html',
                form = form,
                name_to_update = name_to_update)   
    else:
        return render_template('update.html',
            form = form,
            name_to_update = name_to_update)

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
            user = Users(name=form.name.data, email=form.email.data,
                favourite_color=form.favourite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favourite_color.data = ''

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

# Add update.html

# Powershell
# $env:FLASK_APP = "11_migrate_database.py" 
# $env:FLASK_ENV = "development"
# flask run

### without the migration
# UndefinedError
# jinja2.exceptions.UndefinedError: '10_update_record.UserForm object' 
# has no attribute 'favourite_color'

# pip install Flask-Migrate
# flask db init         # create a direcotory file for the migration stuff
# flask db              # show the db command
# flask db migrate -m 'Initial Migration'
# flask db upgrade      # == to migration