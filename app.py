import os

from flask import Flask

from views.categories import categories_view
from views.users import users_view
from views.expenses import expenses_view

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(__file__), 
    'uploads'
    )

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.register_blueprint(categories_view)
app.register_blueprint(users_view)
app.register_blueprint(expenses_view)

