from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin
from flask_migrate import Migrate
# Initialize the Flask app
app = Flask(__name__)

# Set the secret key for the app, used for session management and security (like CSRF protection)
app.config['SECRET_KEY'] = 'your_secret_key'

# Configure the SQLite database URI (using SQLite for simplicity here)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Initialize the SQLAlchemy object for ORM (database interaction)
db = SQLAlchemy(app)

# Initialize Bcrypt for hashing passwords securely
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

# Initialize Flask-Login to manage user sessions and authentication
login_manager = LoginManager(app)

# Define which view to redirect to if a user is not logged in and tries to access a protected route
login_manager.login_view = 'login'

# This callback is used by Flask-Login to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Load the user by ID from the database

# Import models (User and Task) and forms (RegistrationForm, LoginForm, TaskForm) from separate modules
from models import User, Task
from forms import RegistrationForm, LoginForm, TaskForm

# Define the route for the home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')  # Render the home page template

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # If the user is already logged in, redirect them to the tasks page
        return redirect(url_for('tasks'))
    
    form = RegistrationForm()  # Create an instance of the registration form
    
    if form.validate_on_submit():  # If the form is submitted and passes validation
        # Hash the user's password before saving to the database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # Create a new user instance with the form data and the hashed password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        # Add the user to the database and commit the changes
        db.session.add(user)
        db.session.commit()
        
        # Flash a success message and redirect the user to the login page
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)  # Render the registration template with the form

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # If the user is already logged in, redirect to tasks page
        return redirect(url_for('tasks'))
    
    form = LoginForm()  # Create an instance of the login form
    
    if form.validate_on_submit():  # If the form is submitted and passes validation
        # Query the database for a user with the provided email
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check if the user exists and the provided password matches the stored hashed password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Log the user in and redirect them to the tasks page
            login_user(user)
            return redirect(url_for('tasks'))
        else:
            # If login fails, flash an error message
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', form=form)  # Render the login template with the form

# Route for user logout
@app.route('/logout')
def logout():
    logout_user()  # Log out the current user
    return redirect(url_for('home'))  # Redirect to the home page

# Route to display tasks (Create, Read functionality), requires user to be logged in
@app.route('/tasks', methods=['GET', 'POST'])
@login_required  # Ensures that the user must be logged in to access this route
def tasks():
    form = TaskForm()  # Create an instance of the task form
    
    if form.validate_on_submit():  # If the form is submitted and passes validation
        # Create a new task with the form data and associate it with the logged-in user
        task = Task(title=form.title.data, content=form.content.data, user_id=current_user.id)
        
        # Add the task to the database and commit the changes
        db.session.add(task)
        db.session.commit()
        
        # Flash a success message and redirect the user to the tasks page
        flash('Task created!', 'success')
        return redirect(url_for('tasks'))
    
    # Query the database for tasks that belong to the logged-in user
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    return render_template('tasks.html', tasks=tasks, form=form)  # Render the tasks page with the form and task list

# Route to update an existing task, requires user to be logged in
@app.route('/task/<int:task_id>/update', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        abort(403)
    
    form = TaskForm()

    if form.validate_on_submit():
        task.title = form.title.data
        task.content = form.content.data
        db.session.commit()
        flash('Your task has been updated!', 'success')
        return redirect(url_for('tasks'))
    
    elif request.method == 'GET':
        form.title.data = task.title
        form.content.data = task.content

    # Print to check the template name
    print("Rendering template: update_task.html")

    return render_template('update_task.html', form=form,task=task)


# Route to delete an existing task, requires user to be logged in
@app.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required  # Ensures the user must be logged in to access this route
def delete_task(task_id):
    # Retrieve the task by ID or return a 404 error if not found
    task = Task.query.get_or_404(task_id)
    
    # Ensure that only the task's owner can delete it
    if task.user_id != current_user.id:
        abort(403)  # Return a 403 Forbidden error if the user is not authorized
    
    # Delete the task from the database and commit the changes
    db.session.delete(task)
    db.session.commit()
    
    # Flash a success message and redirect to the tasks page
    flash('Your task has been deleted!', 'success')
    return redirect(url_for('tasks'))

# Run the app in debug mode (for development purposes)
if __name__ == '__main__':
    app.run(debug=False)
