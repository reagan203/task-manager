from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# The RegistrationForm class defines the fields and validation rules for the registration form
class RegistrationForm(FlaskForm):
    # A field for the user's username, requiring a minimum length of 2 and a maximum of 20 characters
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    
    # A field for the user's email, ensuring the data is provided and is in a valid email format
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    # A field for the user's password, requiring that the password is provided
    password = PasswordField('Password', validators=[DataRequired()])
    
    # A confirmation field for the password, requiring it to match the original password
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    # A submit button labeled 'Sign Up' to submit the form
    submit = SubmitField('Sign Up')

# The LoginForm class defines the fields and validation rules for the login form
class LoginForm(FlaskForm):
    # A field for the user's email, ensuring it is provided and valid
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    # A field for the user's password, ensuring it is provided
    password = PasswordField('Password', validators=[DataRequired()])
    
    # A submit button labeled 'Login' to submit the form
    submit = SubmitField('Login')

# The TaskForm class defines the fields for adding or updating a task
class TaskForm(FlaskForm):
    # A field for the task's title, requiring that the title is provided
    title = StringField('Title', validators=[DataRequired()])
    
    # A text area for the task's content, ensuring that content is provided
    content = TextAreaField('Content', validators=[DataRequired()])
    
    # A submit button labeled 'Add Task' to submit the form for creating or updating a task
    submit = SubmitField('Add Task')
