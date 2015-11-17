from flask_wtf import Form
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField, DateField
import datetime
from wtforms.validators import DataRequired
import re
paceRegex=re.compile(r'^(([01]\d|2[0-9]):([0-5]\d)|20:00)$')

class RunsFilterForm(Form):
	raceMi=SelectField("Race Dist", choices=[(3.10686, "5k"), (3.10686*2, "10k"), (13.1, 'Half marathon'), (26.2, 'Marathon')], default=(3.10686, "5k"))
	minPace=DecimalField('Min Pace', default=6.0,places=2)
	maxPace=DecimalField('Max Pace', default=15.0, places=2)
	minDist=DecimalField('Min Dist', default=0.5, places=1)
	maxDist=DecimalField('Max Dist', default=15.0, places=1)
	minDate=DateField('Min Date')#, default=(datetime.date.today()), format="%m/%d/%y")
	maxDate=DateField('Max Date')#, default=datetime.date.today(), format="%m/%d/%y")
	submit=SubmitField('Recalculate')
