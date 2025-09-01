# server/__init__.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create extensions (no app yet, so no circular import)
db = SQLAlchemy()
migrate = Migrate()
