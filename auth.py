from flask import Blueprint, request, jsonify, redirect, url_for, render_template, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from models import db, User

auth_bp = Blueprint('auth', __name__)

login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("home"))  # Redirect to your actual homepage
        else:
            flash("Invalid username or password", "error")

    return render_template("login.html")

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("❌ Username already taken!", "error")
            return redirect(url_for("auth.register"))

        # Create new user and hash the password
        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        flash("✅ Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")
