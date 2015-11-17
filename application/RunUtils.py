from stravalib import client, unithelper
import datetime, time, math
from flask_table import *
import RunAnalysis

def minPerMile(meterPerSec):
	secPerMile=unithelper.mile/unithelper.meter/float(meterPerSec)
	return secPerMile/60.
def minAndMax(l):
	return [min(l), max(l)]
def betweenMinMax(val, minMax):
	return val > minMax[0] and val < minMax[1] 
def raceDistInMi(raceDist):
	raceDist=raceDist.lower()
	if raceDist is not None:
		if raceDist=="5k":
			raceMi=3.10686
		elif raceDist=="10k":
			raceMi=2*3.10686
		elif raceDist=="half marathon":
			raceMi=13.2
		elif raceDist=="marathon":
			raceMi=26.2
		else:
			raceMi=None
	return raceMi


class Run:
	def __init__(self, act, raceMi=0):
		self.id=act.id
		self.dist=float(unithelper.miles(act.distance))
		self.time=act.moving_time.seconds
		self.date=act.start_date
		self.startTime=datetime.datetime.strptime(datetime.datetime.strftime(act.start_date, "%H:%M"), "%H:%M")
		self.pace=minPerMile(act.average_speed)
		self.maxPace=minPerMile(act.max_speed)
		self.el=unithelper.feet(act.total_elevation_gain)
		self.name=act.name
		self.raceMi=raceMi
		if raceMi is not None:
			self.predictTimes(raceMi)
		else:
			self.riegelTime=None
			self.cameronTime=None
	def predictTimes(self, raceDist):
		self.riegelTime=RunAnalysis.riegelFormula(raceDist, self.dist, self.time)
		self.cameronTime=RunAnalysis.cameronFormula(raceDist, self.dist, self.time)
	

class RunList:
	def __init__(self, activities=[], raceDist=None):
		raceMi=raceDistInMi(raceDist)
		print "RaceDist init",raceDist
		self.runs=[Run(a, raceMi) for a in activities if self.validRun(a) ]
		self.maxNRuns=1000
		self.setDefRanges()
		self.goodRuns=self.runs
		self.raceMi=3.10686
	def validRun(self, act):
		return float(unithelper.miles(act.distance)) > 0.5 and act.moving_time.seconds > 5.*60 and float(act.average_speed) > 0. and float(act.max_speed) > 0.
	def avgTimeStrs(self):
		avgRiegel=time.strftime('%H:%M:%S', time.gmtime(sum(r.riegelTime for r in self.goodRuns)/len(self.goodRuns)))
		avgCam=time.strftime('%H:%M:%S', time.gmtime(sum(r.cameronTime for r in self.goodRuns)/len(self.goodRuns)))
		return avgRiegel, avgCam

	def setDefRanges(self):
		if len(self.runs) ==0:
			self.dateRange=[datetime.datetime.today()-datetime.timedelta(months=6), datetime.datetime.today()]
			self.paceRange=[0., 20.]
			self.elRange=[-10000, 10000]
			self.startTimeRange=[time.time.strptime("00:00", "%H:%M"), time.time.strptime("23:59", "%H:%M")]
			self.minDist, self.maxDict=[0.5, 50.]
			self.maxNRuns=0
		else:
			self.dateRange=minAndMax([r.date for r in self.runs])
			self.minPace, self.maxPace=minAndMax([r.pace for r in self.runs])
			self.elRange=minAndMax([int(r.el) for r in self.runs])
			self.startTimeRange=minAndMax([r.startTime for r in self.runs])
			self.minDist, self.maxDict=minAndMax([(r.dist) for r in self.runs])
			self.maxNRuns=len(self.runs)
	def filterList(self, raceDist=None):
		self.goodRuns=[]
		if raceDist is None:
			raceMi=float(self.raceMi)
		else:
			raceMi=float(raceDistInMi(raceDist))
		for r in self.runs:
			if len(self.goodRuns) >=self.maxNRuns:
				break
			# if betweenMinMax(r.date, self.dateRange) and betweenMinMax(int(r.pace.split(":")[0]), self.paceRange) and betweenMinMax(int(r.el), self.elRange) and betweenMinMax(r.startTime, self.startTimeRange) and betweenMinMax(r.dist, self.distRange):
			if betweenMinMax(r.dist, [self.minDist, self.maxDist]):
				r.predictTimes(raceMi)
				self.goodRuns.append(r)
		return self.goodRuns
class RunTable(Table):
	classes=["table","table-striped"]
	dist=Col("Distance")
	elTime=Col("Time elapsed")
	date=Col("Date")
	startTime=Col("Start time")
	pace=Col("Avg. Pace")
	maxPace=Col("Max Pace")
	cameron=Col("Cameron Prediction")
	riegel=Col("Riegel Prediction")
	name=Col("Name")
def tableFromRunList(runList):
	items=list()
	for act in runList.goodRuns:
		elTime=time.strftime('%H:%M:%S', time.gmtime(act.time))
		startTime=datetime.datetime.strftime(act.startTime, "%H:%M")
		date=datetime.datetime.strftime(act.date, '%m/%d/%y')
		if act.cameronTime is not None:
			cameronTime=time.strftime('%H:%M:%S', time.gmtime(act.cameronTime))
			riegelTime=time.strftime('%H:%M:%S', time.gmtime(act.riegelTime))
		else:
			cameronTime=riegelTime="n/a"
		items.append(dict(dist=unithelper.miles(act.dist), elTime=elTime, date=date, startTime=startTime, pace=act.pace, maxPace=act.maxPace, el=act.el, name=act.name, cameron=cameronTime, riegel=riegelTime))
		
		#items.append(dict(dist=unithelper.miles(act.dist), elTime=time.time.strftime('%H:%M:%S', time.gmtime(act.time)), date=act.date, startTime=time.time.strftime('%H:%M', act.startTime), pace=act.pace, maxPace=act.maxPace, el=act.total_elevation_gain, name=act.name))
	return RunTable(items)








	


