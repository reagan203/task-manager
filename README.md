Task Manager
Task Manager is a simple web application built with Flask that allows users to create, update, and delete tasks. It also includes user authentication, where users can register and log in to manage their personalized tasks. The app uses SQLite for data storage, Flask-Bcrypt for password hashing, and Flask-Login for managing user sessions.

Table of Contents
Features
Technologies Used
Installation
Usage
Folder Structure
Database Models
Routes
Forms
Contributing
License
Features
User Registration and Login: Users can create an account and log in securely using hashed passwords.
Task Management: Authenticated users can create, update, and delete tasks.
User Sessions: Sessions are managed to ensure only authenticated users can access their own tasks.
Flask-Migrate Integration: Manage database migrations seamlessly.
Form Validation: All forms are validated before submitting.
Task Ownership: Users can only manage tasks they created.
Technologies Used
Flask: Web framework.
Flask-SQLAlchemy: ORM (Object Relational Mapper) for database interactions.
Flask-Bcrypt: For securely hashing passwords.
Flask-Login: For managing user sessions.
Flask-Migrate: For handling database migrations.
SQLite: Lightweight database for development purposes.
Installation
Prerequisites
Make sure you have the following installed on your machine:

Python 3.x
Virtualenv
Steps
Clone the repository

bash
Copy code
git clone  https://github.com/reagan203/task-manager
Navigate to the project directory

bash
Copy code
cd task-manager
Set up a virtual environment

bash
Copy code
python3 -m venv venv
Activate the virtual environment

On Windows:

bash
Copy code
venv\Scripts\activate
On macOS/Linux:

bash
Copy code
source venv/bin/activate
Install dependencies

bash
Copy code
pip install -r requirements.txt
Set up the database

Run the following commands to initialize the database and run the migrations:

bash
Copy code
flask db init
flask db migrate
flask db upgrade
Run the application

bash
Copy code
flask run
Access the app

Open your browser and navigate to http://127.0.0.1:5000/.

Usage
Register an account: Navigate to the /register route and create a new account.
Log in: After registering, log in using your email and password.
Create tasks: Once logged in, you can create tasks on the /tasks page.
Update tasks: You can click on any task to update its title or content.
Delete tasks: You can delete any task by clicking on the "Delete" button next to it.
Folder Structure
bash
Copy code
.
├── app.py              # Main application file
├── models.py           # Database models for users and tasks
├── forms.py            # Form classes for login, registration, and tasks
├── templates/          # HTML templates
│   ├── base.html       # Base layout template
│   ├── home.html       # Home page template
│   ├── login.html      # Login page template
│   ├── register.html   # Registration page template
│   ├── tasks.html      # Task management page
│   ├── update_task.html# Update task page
├── static/             # Static files (CSS, JS)
│   └── styles.css      # Custom CSS styles
├── migrations/         # Database migration files
└── README.md           # This file
Database Models
User Model
The User model represents the users of the application. It includes the following fields:

id: Unique identifier for each user.
username: The name of the user.
email: The email address of the user.
password: The hashed password of the user.
Task Model
The Task model represents tasks created by users. Each task belongs to a user and includes:

id: Unique identifier for each task.
title: The title of the task.
content: The content or description of the task.
user_id: Foreign key linking the task to a specific user.
Routes
/
Method: GET
Description: Renders the home page.
/register
Method: GET, POST
Description: Registers a new user.
Protected: Redirects to /tasks if the user is already logged in.
/login
Method: GET, POST
Description: Logs in an existing user.
Protected: Redirects to /tasks if the user is already logged in.
/logout
Method: GET
Description: Logs out the current user.
/tasks
Method: GET, POST
Description: Displays and allows the user to manage tasks.
Protected: Requires the user to be logged in.
/task/<int:task_id>/update
Method: GET, POST
Description: Updates an existing task.
Protected: Requires the user to be logged in and the task owner.
/task/<int:task_id>/delete
Method: POST
Description: Deletes an existing task.
Protected: Requires the user to be logged in and the task owner.
Forms
RegistrationForm
username: Required field.
email: Required field.
password: Required field with length validation.
confirm_password: Must match the password.
LoginForm
email: Required field.
password: Required field.
TaskForm
title: Required field.
content: Required field.
Contributing
If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Contributions are always welcome!

License
This project is licensed under the MIT License. See the LICENSE file for details.

