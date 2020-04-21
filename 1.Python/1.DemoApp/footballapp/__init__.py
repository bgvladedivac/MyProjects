
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SECRET_KEY = os.urandom(32)


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///footballers.sqlite"


db = SQLAlchemy(app)
from footballapp import routes
from footballapp.models import User, Team
print("I was executed.")

db.create_all()


