from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Initialize the database with Flask app context."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
