from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

schedule_app = Flask(__name__)
schedule_app.config.from_object(Config)
db = SQLAlchemy(schedule_app)
migrate = Migrate(schedule_app, db)




from app import routes, models
