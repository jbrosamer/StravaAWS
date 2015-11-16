from sqlalchemy.ext.declarative import declarative_base
from wtforms_alchemy import ModelForm, ModelFormField
from stravalib import unithelper
import RunUnits as ru
from flask_marshmallow import Marshmallow

Base = declarative_base()

class Run(Base):
	__tablename__='runs'
	id=sa.Column(sa.Integer, primary_key=True)
	dist=sa.Column(sa.Decimal, nullable=False) #distance in miles
	time=sa.Column(sa.Decimal, nullable=False) #moving time in seconds
	date=sa.Column(sa.Decimal, nullable=False)
	startTime=sa.Column(sa.DateTime, nullable=False) #time of day started
	pace=sa.Column(sa.Time, nullable=False)
	maxPace=sa.Column(sa.Time, nullable=False)
	elevation=sa.Column(sa.Decimal, nullable=False) #elevation in feet
	name=sa.Column(sa.Decimal, nullable=False) #user's name for run
	def __init__(self, act):
		self.id=act.id
		self.dist=float(unithelper.miles(act.distance))
		self.time=act.moving_time.seconds
		self.date=act.start_date
		self.startTime=act.start_date, "%H:%M"), "%H:%M"
		self.pace=ru.minPerMile(act.average_speed)
		self.maxPace=ru.minPerMile(act.max_speed)
		self.el=unithelper.feet(act.total_elevation_gain)
		self.name=act.name


class RacePrediction(Base):
	__tablename__='racepred'
	id=sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	raceMi=sa.Column(sa.Decimal, nullable=False, default=1.0)
	runId=sa.Column(sq.Integer, sa.ForeignKey(Run.id))
	run=sa.orm.relationship(Run)
	cameronTime=sa.Column(sa.Time, nullable=True, onupdate=time.gmtime(ru.cameronTime(self.raceMi, self.run.dist, self.run.time)))
	riegelTime=sa.Column(sa.Time, nullable=True, onupdate=time.gmtime(ru.riegelTime(self.raceMi, self.run.dist, self.run.time)))
	def __init__(self, run, raceMi=None):
		self.runId=run.id
		self.raceMi=raceMi
		self.riegelTime=self.getPrediction('r')
		self.cameronTime=self.getPrediction('c')
	def getPrediction(self, predModel='r'):
		if predModel=='r':
			return time.gmtime(ru.riegelTime(self.raceMi, self.run.dist, self.run.time))
		else:
			return time.gmtime(ru.cameronTime(self.raceMi, self.run.dist, self.run.time))
class RunFilter(Base):
	__tablename__='runfilter'