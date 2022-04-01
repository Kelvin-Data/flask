from flask import Flask, render_template

# Create a Flask Instance
app = Flask(__name__) # help flask find the directory & file

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

# Powershell
# $env:FLASK_APP = "3_error.py" 
# $env:FLASK_ENV = "development"
# flask run

### ACTIVATE THE VENV ###
# venv_flask\Scripts\activartevenv\Scripts\activate

### SET UP A SSH KEYS ###
# deactivate # VENV
# cd ~/
# pwd
# mkdir .ssh
# cd .ssh
# pwd
# ssh-keygen.exe
# ls
# cat id_rsa.pub
# In Github - click setting insert the id_rsa.pub

### INITIALISE THE GITHUB ###
# git config --global user.name "Kelvin-Data"
# git config --global user.email "bhlohass@gmail.com"
# git config --global push.default matching
# git config --global alias.co checkout
# git init

### ADD FILE TO GITHUB ###
# git add .
# git commit -am 'initial commit' # saving your code

# In Github - click your reponsitories 
# Type the reponsitories name 
# click the create reponsitories

### PUSH EXISTING REPOSITORIES ###
# git remote add origin https://github.com/Kelvin-Data/flask.git
# git branch -M main
# git push -u origin main

### CHANGE FILE & ADD TO GITHUB ###
# git add .