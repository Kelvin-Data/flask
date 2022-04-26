from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Create a Flask Instance
app = Flask(__name__) # help flask find the directory & file
app.config['SECRET_KEY'] = 'my super secret key that no one is supposed to know'

# Create form class
class NameForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit =SubmitField("Submit")

# Create a route decorator
@app.route('/') # url www.about.html

# def index():
#    return "<h1>Hello World!</h1>"

def index():
    first_name = 'John'
     # stuff = 'This is <strong>Bold</strong> Text!' # for the striptags
    stuff = 'This is bold Text!'  # for the title

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
    return render_template('name.html',
        name = name,
        form = form)

### Class Field ###            ### Validators ###
# BooleanField                 # DateRequired
# DateField                    # Email
# DateTimeField                # EqualTo
# DecimalField                 # InputRequired
# FileField                    # IPAddress
# HiddenField                  # Length
# MultipleField                # MacAddress
# FieldList                    # NumberRange
# FloatField                   # Optional
# FormField                    # Regexp
# IntegerField                 # URL 
# PasswordField                # AnyOf
# RadioField                   # NoneOf
# SelectField
# SelectMultipleField
# SubmitField
# StringField
# TextAreaField

# https://flask-wtf.readthedocs.io/en/1.0.x/

# add name.html
# add class nameForm

# Powershell
# $env:FLASK_APP = "5_wtf.py" 
# $env:FLASK_ENV = "development"
# flask run