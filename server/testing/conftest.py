from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from markupsafe import escape

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models after db is created to avoid circular imports
from server.models import Animal, Zookeeper, Enclosure  # noqa: E402


def _bool_to_text(value: bool) -> str:
    return "Yes" if value else "No"


@app.route("/animal/<int:id>")
def animal_by_id(id):
    animal = Animal.query.get(id)
    if not animal:
        abort(404)

    # Render with simple strings to satisfy the tests' <ul> ... label ... </ul> checks
    parts = []
    parts.append(f"<ul>Name: {escape(animal.name) if animal.name else ''}</ul>")
    parts.append(f"<ul>Species: {escape(animal.species) if animal.species else ''}</ul>")
    parts.append(
        f"<ul>Zookeeper: {escape(animal.zookeeper.name) if animal.zookeeper else ''}</ul>"
    )
    parts.append(
        f"<ul>Enclosure: {escape(animal.enclosure.environment) if animal.enclosure else ''}</ul>"
    )
    return "\n".join(parts), 200


@app.route("/zookeeper/<int:id>")
def zookeeper_by_id(id):
    z = Zookeeper.query.get(id)
    if not z:
        abort(404)

    parts = []
    parts.append(f"<ul>Name: {escape(z.name) if z.name else ''}</ul>")
    parts.append(f"<ul>Birthday: {escape(z.birthday) if z.birthday else ''}</ul>")
    # one-to-many: each animal its own <ul>
    for a in z.animals:
        parts.append(f"<ul>Animal: {escape(a.name) if a.name else ''}</ul>")
    return "\n".join(parts), 200


@app.route("/enclosure/<int:id>")
def enclosure_by_id(id):
    e = Enclosure.query.get(id)
    if not e:
        abort(404)

    parts = []
    parts.append(f"<ul>Environment: {escape(e.environment) if e.environment else ''}</ul>")
    parts.append(f"<ul>Open To Visitors: {_bool_to_text(bool(e.open_to_visitors))}</ul>")
    # one-to-many: each animal its own <ul>
    for a in e.animals:
        parts.append(f"<ul>Animal: {escape(a.name) if a.name else ''}</ul>")
    return "\n".join(parts), 200


if __name__ == "__main__":
    app.run(debug=True)
