from flask import jsonify
from server.app import app  # ✅ fixed import
from server.models import db, Animal, Zookeeper, Enclosure  # ✅ fixed import

@app.route("/animal/<int:id>")
def animal_by_id(id):
    animal = Animal.query.get(id)
    if not animal:
        return "<h1>Animal not found</h1>", 404

    return f"""
        <ul>
            <li>ID: {animal.id}</li>
            <li>Name: {animal.name}</li>
            <li>Species: {animal.species}</li>
            <li>Zookeeper: {animal.zookeeper.name if animal.zookeeper else 'None'}</li>
            <li>Enclosure: {animal.enclosure.environment if animal.enclosure else 'None'}</li>
        </ul>
    """

@app.route("/zookeeper/<int:id>")
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get(id)
    if not zookeeper:
        return "<h1>Zookeeper not found</h1>", 404

    animal_list = "".join(
        f"<li>{animal.name} the {animal.species}</li>" for animal in zookeeper.animals
    )

    return f"""
        <ul>
            <li>Name: {zookeeper.name}</li>
            <li>Birthday: {zookeeper.birthday}</li>
            <li>Animals:</li>
            <ul>{animal_list}</ul>
        </ul>
    """

@app.route("/enclosure/<int:id>")
def enclosure_by_id(id):
    enclosure = Enclosure.query.get(id)
    if not enclosure:
        return "<h1>Enclosure not found</h1>", 404

    animal_list = "".join(
        f"<li>{animal.name} the {animal.species}</li>" for animal in enclosure.animals
    )

    return f"""
        <ul>
            <li>Environment: {enclosure.environment}</li>
            <li>Open to Visitors: {'Yes' if enclosure.open_to_visitors else 'No'}</li>
            <li>Animals:</li>
            <ul>{animal_list}</ul>
        </ul>
    """

