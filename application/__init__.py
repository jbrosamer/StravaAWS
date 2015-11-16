from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from pint import UnitRegistry

ureg = UnitRegistry()
application = Flask(__name__)
application.config.from_object('config')
db = SQLAlchemy(application)
