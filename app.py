import pymysql
pymysql.install_as_MySQLdb()
from flask import flash, session, url_for

from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from auth import auth_bp
from models import db, User, Livestock

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1234@localhost/livestock_db"
app.config["SECRET_KEY"] = "supersecretkey"

db.init_app(app)  # Initialize database
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

app.register_blueprint(auth_bp, url_prefix="/auth")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    livestock_data = db.session.query(
        Livestock.id,
        Livestock.species,
        Livestock.breed,
        Livestock.age,
        Livestock.weight
    ).all()
    return render_template('index.html', livestock=livestock_data)

@app.route('/submit', methods=['POST'])
def submit():
    species = request.form.get('species')
    breed = request.form.get('breed')
    age = request.form.get('age')
    weight = request.form.get('weight')

    if not species or not breed or not age or not weight:
        flash("All fields are required!", "error")
        return redirect(url_for('index'))

    new_animal = Livestock(species=species, breed=breed, age=int(age), weight=float(weight))
    db.session.add(new_animal)
    db.session.commit()

    flash("Livestock added successfully!", "success")
    return redirect(url_for('index'))

@app.route('/livestock', methods=['GET'])
@login_required
def get_all_livestock():
    livestock_list = Livestock.query.all()
    return jsonify([{
        "id": l.id,
        "animal_name": l.animal_name,
        "breed": l.breed,
        "age": l.age,
        "health_status": l.health_status
    } for l in livestock_list])

@app.route('/register', methods=['POST'])
def register():
    # Registration logic here
    flash('Registration successful! Welcome aboard.', 'success')
    return redirect(url_for('auth.login'))

@app.route('/add_livestock', methods=['POST'])
@login_required
def add_livestock():
    name = request.form['animal_name']
    breed = request.form['breed']
    age = request.form['age']
    health_status = request.form['health_status']

    new_animal = Livestock(
        animal_name=name,
        breed=breed,
        age=int(age),
        health_status=health_status
    )
    db.session.add(new_animal)
    db.session.commit()
    
    flash('Livestock record added successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables exist
    app.run(debug=True, host='0.0.0.0', port=5000)
