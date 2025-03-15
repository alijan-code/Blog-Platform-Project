from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')

# Create upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    posts = db.relationship('BlogPost', backref='author', lazy=True)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    views = db.Column(db.Integer, default=0)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/')
def index():
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('You do not have permission to access the admin panel.', 'danger')
        return redirect(url_for('index'))
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('admin.html', posts=posts)

@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    if not current_user.is_admin:
        flash('You do not have permission to add posts.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.files.get('image')
        image_url = None
        
        try:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                image_url = f'uploads/{filename}'
                
            post = BlogPost(
                title=title,
                content=content,
                image_url=image_url,
                user_id=current_user.id
            )
            db.session.add(post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating post: {str(e)}', 'danger')
            
    return render_template('add_post.html')

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    if not current_user.is_admin:
        flash('You do not have permission to edit posts.', 'danger')
        return redirect(url_for('index'))
        
    post = BlogPost.query.get_or_404(post_id)
    
    if request.method == 'POST':
        try:
            post.title = request.form.get('title')
            post.content = request.form.get('content')
            image = request.files.get('image')
            
            if image and allowed_file(image.filename):
                if post.image_url:
                    old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], post.image_url.split('/')[-1])
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                post.image_url = f'uploads/{filename}'
                
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating post: {str(e)}', 'danger')
            
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    if not current_user.is_admin:
        flash('You do not have permission to delete posts.', 'danger')
        return redirect(url_for('index'))
        
    post = BlogPost.query.get_or_404(post_id)
    try:
        if post.image_url:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], post.image_url.split('/')[-1])
            if os.path.exists(image_path):
                os.remove(image_path)
        
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting post: {str(e)}', 'danger')
        
    return redirect(url_for('admin'))

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    post.views += 1
    db.session.commit()
    # Get previous and next posts
    prev_post = BlogPost.query.filter(BlogPost.id < post_id).order_by(BlogPost.id.desc()).first()
    next_post = BlogPost.query.filter(BlogPost.id > post_id).order_by(BlogPost.id.asc()).first()
    
    return render_template('post.html', post=post, prev_post=prev_post, next_post=next_post)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Here you would typically send an email or save to database
        # For now, we'll just show a success message
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
        
    return render_template('contact.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            try:
                db.session.commit()
                print("Admin user created successfully!")
            except Exception as e:
                db.session.rollback()
                print(f"Error creating admin user: {str(e)}")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
