import re
import pytest

from app import app, db
from server.models import Animal, Enclosure, Zookeeper


@pytest.fixture(scope="module")
def client():
    """Flask test client with a fresh database."""
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create test data
        a1 = Animal(name="Leo", species="Lion")
        a2 = Animal(name="Mia", species="Tiger")
        e = Enclosure(environment="Savannah", open_to_visitors=True)
        z = Zookeeper(name="John", birthday="1980-05-12")

        e.animals = [a1, a2]
        z.animals = [a1, a2]

        db.session.add_all([a1, a2, e, z])
        db.session.commit()

        yield app.test_client()

        db.drop_all()


class TestApp:
    '''Flask application in app.py'''

    def test_animal_route(self, client):
        '''has a resource available at "/animal/<id>".'''
        animal = Animal.query.first()
        response = client.get(f'/animal/{animal.id}')
        assert response.status_code == 200

    def test_animal_route_has_attrs(self, client):
        '''displays attributes in animal route in <ul> tags called Name, Species.'''
        animal = Animal.query.first()
        response = client.get(f'/animal/{animal.id}')
        html = response.data.decode()

        assert re.search(r"<ul>.*Name.*</ul>", html, re.DOTALL)
        assert re.search(r"<ul>.*Species.*</ul>", html, re.DOTALL)

    def test_animal_route_has_many_to_one_attrs(self, client):
        '''displays attributes in animal route in <ul> tags called Zookeeper, Enclosure.'''
        animal = Animal.query.first()
        response = client.get(f'/animal/{animal.id}')
        html = response.data.decode()

        assert re.search(r"<ul>.*Zookeeper.*</ul>", html, re.DOTALL)
        assert re.search(r"<ul>.*Enclosure.*</ul>", html, re.DOTALL)

    def test_zookeeper_route(self, client):
        '''has a resource available at "/zookeeper/<id>".'''
        zookeeper = Zookeeper.query.first()
        response = client.get(f'/zookeeper/{zookeeper.id}')
        assert response.status_code == 200

    def test_zookeeper_route_has_attrs(self, client):
        '''displays attributes in zookeeper route in <ul> tags called Name, Birthday.'''
        zookeeper = Zookeeper.query.first()
        response = client.get(f'/zookeeper/{zookeeper.id}')
        html = response.data.decode()

        assert re.search(r"<ul>.*Name.*</ul>", html, re.DOTALL)
        assert re.search(r"<ul>.*Birthday.*</ul>", html, re.DOTALL)

    def test_zookeeper_route_has_one_to_many_attr(self, client):
        '''displays attributes in zookeeper route in <ul> tags called Animal.'''
        zookeeper = Zookeeper.query.first()
        response = client.get(f'/zookeeper/{zookeeper.id}')
        html = response.data.decode()

        assert re.search(r"<ul>.*Animal.*</ul>", html, re.DOTALL)

    def test_enclosure_route(self, client):
        '''has a resource available at "/enclosure/<id>".'''
        enclosure = Enclosure.query.first()
        response = client.get(f'/enclosure/{enclosure.id}')
        assert response.status_code == 200

    def test_enclosure_route_has_attrs(self, client):
        '''displays attributes in enclosure route in <ul> tags called Environment, Open to Visitors.'''
        enclosure = Enclosure.query.first()
        response = client.get(f'/enclosure/{enclosure.id}')
        html = response.data.decode()

        assert re.search(r"<ul>.*Environment.*</ul>", html, re.DOTALL)
        assert re.search(r"<ul>.*Open\s*to\s*Visitors.*</ul>", html, re.DOTALL)

    def test_enclosure_route_has_one_to_many_attr(self, client):
        '''displays attributes in enclosure route in <ul> tags called Animal.'''
        enclosure = Enclosure.query.first()
        response = client.get(f'/enclosure/{enclosure.id}')
        html = response.data.decode()

        assert re.search(r"<ul>.*Animal.*</ul>", html, re.DOTALL)
