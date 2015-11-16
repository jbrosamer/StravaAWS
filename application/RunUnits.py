import numpy as numpy
from datetime import datetime, time
from stravalib import unithelper
import math



def riegelFormula(newDist, oldDist, oldTime):
	return oldTime*math.pow(newDist/oldDist, 1.06)

def cameronFormula(newDist, oldDist, oldTime):
	a=13.49681-(0.000030363*oldDist)+(835.7114/math.pow(oldDist, 0.7905))
	b=13.49681-(0.000030363*newDist)+(835.7114/math.pow(newDist, 0.7905))
	return (oldTime/oldDist)*(a/b)*newDist

def paceToStr(t):
	return datetime.time.strftime("%M:%S", t)
def datetimeToTime(dt):
	return datetime.strptime("%H:%M", dt)
def secondsToTime(s):
	return datetime.time.gmtime(s)
def minPerMile(meterPerSec):
	secPerMile=unithelper.mile/unithelper.meter/float(meterPerSec)
	return time.strftime('%M:%S', time.gmtime(secPerMile))