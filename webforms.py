from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

# Create login form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Submit')

# Create posts form
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    #content = StringField('Content', validators=[DataRequired()], 
    #    widget=TextArea())
    content = CKEditorField('Content', validators=[DataRequired()])
    author = StringField('Author') # validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Create form class
class NameForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit =SubmitField("Submit")

# Create form class
class PasswordForm(FlaskForm):
    email = StringField("What's Your Email", validators=[DataRequired()])
    password_hash = PasswordField("What's Your Password", validators=[DataRequired()])
    submit =SubmitField("Submit")

# Create a search form
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField('Submit')

# Create form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favourite_color = StringField("Favourite Color")
    about_author = TextAreaField("About Author")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo(
        'password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    profile_pic = FileField('Profile Pic')
    submit =SubmitField("Submit")

# When change in the database, you need to migrate the database