from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "This is working!!"

# $env:FLASK_APP = "app.py" 
# $env:FLASK_ENV = "development"
# flask run

# heroku login
# heroku git:remote -a great112

# git init 
# git commit -am 'geat'
# git add .
# git push heroku main