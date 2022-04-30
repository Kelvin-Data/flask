from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "This is working!!"

# $env:FLASK_APP = "app.py" 
# $env:FLASK_ENV = "development"
# flask run

# heroku login

# git init 
# heroku git:remote -a great112

# git add .
# git commit -am "make it better"
# git push heroku main

# heroku git:remote -a great112