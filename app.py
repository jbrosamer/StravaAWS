#!/usr/bin/python

import flask
import logging
import stravalib, tempfile
import os, sys
from flask.ext.sqlalchemy import SQLAlchemy




sys.path.append("./application")
import RunUtils
from forms import RunsFilterForm

defNRuns=100
app = flask.Flask(__name__)
app.runList=None
app.athlete=None
app.predString=''

if os.environ.get('FIXSTRAVA_CONFIG') is None:
    os.environ['FIXSTRAVA_CONFIG']='settings.txt'
app.config.from_envvar('FIXSTRAVA_CONFIG')

logging.basicConfig(level=logging.INFO)


@app.route("/images")
def images():
    import datetime
    import StringIO
    import random
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter
    fig=Figure()
    ax1=fig.add_subplot(121)
    ax2=fig.add_subplot(122, sharey=ax1)
    
    dates=[r.date for r in app.runList.goodRuns]
    dist=[r.dist for r in app.runList.goodRuns]
    riegel=[r.riegelTime/60. for r in app.runList.goodRuns]
    cameron=[r.cameronTime/60. for r in app.runList.goodRuns]
    ymin=min(cameron+riegel)
    ymax=max(cameron+riegel)
    ax1.plot_date(dates, cameron,c='b')
    ax1.plot_date(dates, riegel,c='r')

    ax1.xaxis.set_major_formatter(DateFormatter('%m-%d'))
    c=ax2.scatter(dist, cameron, c='b')
    r=ax2.scatter(dist, riegel, c='r')
    fig.autofmt_xdate()
    ax1.set_ylim([ymin-1.0, ymax+1.0])
    ax2.set_ylim([ymin-1.0, ymax+1.0])
    ax1.set_ylabel("Predicted time (min)")
    ax1.set_xlabel("Date")
    ax2.set_xlabel("Distance (mi)")

    fig.legend([r,c], ["Riegel", "Cameron"])
    canvas=FigureCanvas(fig)
    f = tempfile.NamedTemporaryFile(
     dir='static/temp',
     suffix='.png',delete=False)
    canvas.print_png(f)
    f.close()

    form=RunsFilterForm(obj=app.runList)
    return flask.render_template('image.html', athlete=app.athlete, predString=app.predString, form=form, plotPng="static/temp/"+f.name.split("/")[-1]) 


@app.route('/login')
def login():
    client = stravalib.client.Client()
    form=RunsFilterForm()
    auth_url = client.authorization_url(client_id=app.config['CLIENT_ID'],
            scope='write',
            redirect_uri='http://127.0.0.1:7123/auth')
    return flask.render_template('login.html', auth_url=auth_url)

@app.route('/logout')
def logout():
    flask.session.pop('access_token')
    return flask.redirect(flask.url_for('runs'))

@app.route('/update')
def update():
    return flask.render_template('update.html')

@app.route('/calc', methods=['POST'])
def calc():
    form=RunsFilterForm()
    print "Form minDist",form.minDist.data
    form.populate_obj(app.runList)
    print "Run minDist",app.runList.minDist
    #if form.raceDist.data[1]
    app.runList.filterList()
    return flask.redirect(flask.url_for('runs'))



@app.route('/')
@app.route('/runs', methods=['GET', 'POST'])
def runs():
    if 'access_token' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    if app.athlete is None:
        client = stravalib.client.Client(access_token=flask.session['access_token'])
        app.athlete = client.get_athlete()
    #runList=client.get_activities(limit=10)
    if app.runList is None:
        app.runList=RunUtils.RunList(client.get_activities(limit=defNRuns), raceDist="5k")
    form=RunsFilterForm(obj=app.runList)
    images()
    avgRiegel, avgCam=app.runList.avgTimeStrs()
    app.predString=flask.Markup("<h3>Average predictions for %s miles</h3>\n <h4>Riegel formula: %s</h4>\n <h4>Cameron formula %s</h4>\n"%(form.raceMi.data, avgRiegel, avgCam))
    table=RunUtils.tableFromRunList(app.runList)

    return flask.render_template('runs.html', athlete=app.athlete, predString=app.predString, form=form, table=table)    

@app.route('/auth')
def auth_done():
    # TODO: check for errors 
    code = flask.request.args.get('code', '')
    client = stravalib.client.Client()
    token = client.exchange_code_for_token(client_id=app.config['CLIENT_ID'],
            client_secret=app.config['CLIENT_SECRET'],
            code = code)
    flask.session['access_token'] = token
    return flask.redirect(flask.url_for('runs'))

if __name__ == '__main__':
    app.run(debug=False, port=7123)#, host='0.0.0.0')
