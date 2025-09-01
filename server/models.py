from app import db# server/__init__.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create extensions (no app yet, so no circular import)
db = SQLAlchemy()
migrate = Migrate()


# --- Models ---

class Zookeeper(db.Model):
    __tablename__ = "zookeepers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    birthday = db.Column(db.String)

    animals = db.relationship("Animal", back_populates="zookeeper", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Zookeeper id={self.id} name={self.name!r}>"


class Enclosure(db.Model):
    __tablename__ = "enclosures"

    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String)  # e.g. grass, sand, water
    open_to_visitors = db.Column(db.Boolean, default=True)

    animals = db.relationship("Animal", back_populates="enclosure", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Enclosure id={self.id} environment={self.environment!r}>"


class Animal(db.Model):
    __tablename__ = "animals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    species = db.Column(db.String)

    zookeeper_id = db.Column(db.Integer, db.ForeignKey("zookeepers.id"))
    enclosure_id = db.Column(db.Integer, db.ForeignKey("enclosures.id"))

    zookeeper = db.relationship("Zookeeper", back_populates="animals")
    enclosure = db.relationship("Enclosure", back_populates="animals")

    def __repr__(self):
        return f"<Animal id={self.id} name={self.name!r} species={self.species!r}>"
