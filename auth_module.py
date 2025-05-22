from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

auth_bp = Blueprint('auth', __name__)

submitted_data = []  # Temporary storage for livestock data

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("auth.index"))
        else:
            flash("Invalid username or password!", "error")

    return render_template("login.html")

@auth_bp.route("/index")
@login_required
def index():
    from models import Livestock  # Import here to avoid circular imports if needed
    livestock_data = Livestock.query.with_entities(Livestock.id, Livestock.species).all()
    return render_template("index.html", livestock=livestock_data)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already taken!", "error")
            return redirect(url_for('auth.register'))

        # Create new user
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/submit', methods=['POST'])
@login_required
def submit():
    data = {
        "species": request.form.get("species"),
        "breed": request.form.get("breed"),
        "age": request.form.get("age"),
        "health_status": request.form.get("health_status")
    }
    submitted_data.append(data)  # Store data
    return redirect(url_for('auth.index'))  # Redirect to home page
