from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models, errors
from app.models import Tutor, Booking

db.create_all()

@app.shell_context_processor
def make_shell_context():
    """ Импортировать по умолчанию объекты для работы из консоли """
    return {'db': db, 'Tutor': Tutor, 'Booking': Booking}

