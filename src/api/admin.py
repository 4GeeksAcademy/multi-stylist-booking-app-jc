import os
import inspect
from flask_admin import Admin
from . import models
from .models import db
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    admin = Admin(app, name='Stylist Booking App',
                  theme=Bootstrap4Theme(swatch='cerulean'))
    # admin.add_view(ModelView(User, db.session))
    # admin.add_view(ModelView(Stylist, db.session))
    # admin.add_view(ModelView(Client, db.session))
    # admin.add_view(ModelView(Services, db.session))
    # admin.add_view(ModelView(Availability, db.session))
    # admin.add_view(ModelView(Appointments, db.session))
    # admin.add_view(ModelView(Messages, db.session))
    # admin.add_view(ModelView(Review, db.session))

    # Dynamically add all models to the admin interface
    for name, obj in inspect.getmembers(models):
        # Verify that the object is a SQLAlchemy model before adding it to the admin.
        if inspect.isclass(obj) and issubclass(obj, db.Model):
            admin.add_view(ModelView(obj, db.session))
