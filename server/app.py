from flask import Flask
from server import db, migrate   # ✅ db comes from __init__.py
from server.models import Animal, Zookeeper, Enclosure

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    return app

app = create_app()
