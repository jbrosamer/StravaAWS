from stravalib import client, unithelper
import datetime
from flask_table import create_table, Col, DatetimeCol
tableCls=create_table()\
	.add_column("dist", Col("Dist"))\
	.add_column("date", DatetimeCol("Date"))\
	.add_column("time", DatetimeCol("Time"))\
	.add_column("pace", Col("Avg. Pace"))\
	.add_column("maxPace", Col("Max Pace"))\
	.add_column("el", Col("Elevation"))\
	.add_column("name", Col("Name"))

def minPerMile(meterPerSec):
	secPerMile=1609.34/float(meterPerSec)
	return str(datetime.timedelta(seconds=secPerMile))



def runsToTable(runList):
	items=list()
	for act in runList:
		items.append(dict(dist=unithelper.miles(act.distance), time=act.moving_time.seconds, date=act.start_date, pace=minPerMile(act.average_speed), maxPace=minPerMile(act.max_speed), el=act.total_elevation_gain, name=act.name))
	return tableCls(items)
	


