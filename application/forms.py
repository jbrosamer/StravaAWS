from flask_wtf import Form
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField, DateField
import datetime
from wtforms.validators import DataRequired

class RunsFilterForm(Form):
	raceMi=SelectField("Race Dist", choices=[(3.10686, "5k"), (3.10686*2, "10k"), (13.1, 'Half marathon'), (26.2, 'Marathon')], default=(3.10686, "5k"))
	minPace=DecimalField('Min Pace', default=5)
	maxPace=DecimalField('Max Pace', default=30)
	minDist=DecimalField('Min Dist', default=0.5)
	maxDist=DecimalField('Max Dist', default=15.0)
	minDate=DateField('Min Date')#, default=(datetime.date.today()), format="%m/%d/%y")
	maxDate=DateField('Max Date')#, default=datetime.date.today(), format="%m/%d/%y")
	submit=SubmitField('Recalculate')
