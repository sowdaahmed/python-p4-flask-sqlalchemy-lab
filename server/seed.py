from app import app, db
from server.models import Animal, Zookeeper, Enclosure

def run():
    with app.app_context():
        db.drop_all()
        db.create_all()

        z1 = Zookeeper(name="Dylan Taylor", birthday="1990-06-12")
        z2 = Zookeeper(name="Stephanie Contreras", birthday="1996-09-20")

        e1 = Enclosure(environment="trees", open_to_visitors=True)
        e2 = Enclosure(environment="pond", open_to_visitors=False)

        a1 = Animal(name="Logan", species="Snake", zookeeper=z1, enclosure=e1)
        a2 = Animal(name="Mia", species="Tiger", zookeeper=z1, enclosure=e1)
        a3 = Animal(name="Bubbles", species="Fish", zookeeper=z2, enclosure=e2)

        db.session.add_all([z1, z2, e1, e2, a1, a2, a3])
        db.session.commit()

        print("Seeded database.")

if __name__ == "__main__":
    run()
