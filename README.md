# Blog-Platform-Project
Introduction

This project is a fully functional blog platform built using Flask, a micro web framework for Python. It includes features such as user authentication, admin controls, post management, and image uploads. The platform allows users to read blog posts, while admin users can create, edit, and delete posts. The database is managed using SQLAlchemy, and user authentication is handled via Flask-Login.

Technologies Used

Flask (3.0.0): The main web framework for handling HTTP requests and rendering templates.

Flask-SQLAlchemy (3.1.1): ORM (Object Relational Mapper) for managing the SQLite database.

Flask-Login (0.6.3): Authentication and user session management.

Werkzeug (3.0.1): Password hashing and security features.

python-dotenv (1.0.0): For managing environment variables.

Project Structure

The project consists of multiple Python scripts and supporting files:

app.py: Main application file handling routing, authentication, and database interactions.

migrate_db.py: Script for managing database migrations.

requirements.txt: Specifies dependencies required for the project.

Database Design

User Model

The User model contains the following fields:

id: Primary key (integer).

username: Unique username (string, max 80 characters).

password_hash: Securely stored hashed password.

is_admin: Boolean flag indicating if the user is an admin.

posts: Relationship with the BlogPost model (one-to-many).

BlogPost Model

The BlogPost model contains:

id: Primary key (integer).

title: Post title (string, max 100 characters).

content: Post content (text).

image_url: URL of the uploaded image.

date_posted: Timestamp of post creation.

user_id: Foreign key linking to the User table.

views: Counter for post views.

Features

User Authentication

Users can log in using a username and password.

Passwords are securely stored using generate_password_hash() and check_password_hash() from Werkzeug.

The login_manager.user_loader function ensures user sessions persist across requests.

Admin Panel

Only admins can access the admin dashboard.

Admins can create, edit, and delete posts.

Unauthorized users are redirected to the homepage with an error message.

Blog Post Management

Admins can create new posts with titles, content, and optional images.

Uploaded images are saved securely in the static/uploads directory.

Posts can be edited and updated, including replacing existing images.

Posts can be deleted, with associated images removed from storage.

Blog Navigation

Users can browse posts, sorted by creation date.

Clicking on a post displays the full content and increases its view count.

Previous and next post navigation is available.

Contact Form

Users can submit messages via a contact form.

Messages are displayed in the UI as a confirmation but are not stored in the database.

Database Initialization

The init_db() function ensures database tables are created before running the application.

An admin account is automatically created if it does not exist.

The migrate_db.py script can be used to reset the database.

Running the Project

Install dependencies: pip install -r requirements.txt.

Run the migration script: python migrate_db.py.

Start the application: python app.py.

Access the website at http://127.0.0.1:5000/.

Security Considerations

Passwords are never stored in plaintext.

Only admin users have permissions to modify content.

Image uploads are validated to prevent security risks.

Conclusion

This project provides a robust, scalable blog platform with essential CRUD functionalities, authentication, and an intuitive UI. It serves as a strong foundation for further enhancements, such as comment systems, user roles, and API integrations.

