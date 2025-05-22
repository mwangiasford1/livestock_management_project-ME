from flask import Flask, render_template
from flask_login import LoginManager, login_required
from flask_migrate import Migrate
from extensions import db  # Ensure db is imported correctly
from auth_module import auth_bp  # Import the correct blueprint
from models import User, Livestock  # Import the User and Livestock models

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1234@localhost/livestock_db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "supersecretkey"

    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize Flask-Migrate

    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp, url_prefix='/auth')  # Register the auth blueprint

    @app.route("/")
    @login_required
    def index():
        livestock_data = Livestock.query.with_entities(Livestock.id, Livestock.species).all()
        return render_template("index.html", livestock=livestock_data)

    return app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
