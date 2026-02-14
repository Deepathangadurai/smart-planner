from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURATION ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'deepa-smart-planner-secret' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- LOGIN MANAGER ---
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- DATABASE MODELS ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Todo', backref='owner', lazy=True)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(20), default='Daily')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# --- AUTH ROUTES ---

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if user already exists to prevent IntegrityError
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('signup'))

        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- DASHBOARD ROUTES ---

@app.route('/')
@login_required
def index():
    # Dynamic Greeting Logic
    hour = datetime.now().hour
    if hour < 12: greeting = "Good morning"
    elif 12 <= hour < 18: greeting = "Good afternoon"
    else: greeting = "Good evening"

    # Data Science Stats Logic
    user_tasks = Todo.query.filter_by(user_id=current_user.id).all()
    stats = {}
    for cat in ['Daily', 'Weekly', 'Monthly']:
        total = Todo.query.filter_by(category=cat, user_id=current_user.id).count()
        done = Todo.query.filter_by(category=cat, complete=True, user_id=current_user.id).count()
        stats[cat] = {'percent': int((done/total)*100) if total > 0 else 0}
    
    return render_template('index.html', 
                           tasks=user_tasks, 
                           stats=stats, 
                           name=current_user.username, 
                           greeting=greeting)

@app.route('/add', methods=['POST'])
@login_required
def add():
    task_text = request.form.get('task_content')
    task_cat = request.form.get('category')
    if task_text:
        new_task = Todo(task=task_text, category=task_cat, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:todo_id>')
@login_required
def update(todo_id):
    todo = Todo.query.get(todo_id)
    if todo and todo.user_id == current_user.id:
        todo.complete = not todo.complete
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
@login_required
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo and todo.user_id == current_user.id:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)