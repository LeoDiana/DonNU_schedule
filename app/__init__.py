from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

schedule_app = Flask(__name__)
schedule_app.config.from_object(Config)
db = SQLAlchemy(schedule_app)


from app import routes, models
