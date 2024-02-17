from flask import Flask
from application.config import Config
from application.database import db

app = None

# Create app
def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()

from application.auth import *
from application.views import *

# Create DB
def create_database(app):
    with app.app_context():
        db.create_all()

# Run app
if __name__ == '__main__':
    create_database(app)
    app.run()