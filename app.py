#!/usr/bin/python

import flask
import logging
import stravalib
import os, sys




sys.path.append("./application")
import RunUtils
from forms import RunsFilterForm

defNRuns=10
app = flask.Flask(__name__)
app.runList=None
app.athlete=None

if os.environ.get('FIXSTRAVA_CONFIG') is None:
    os.environ['FIXSTRAVA_CONFIG']='settings.txt'
app.config.from_envvar('FIXSTRAVA_CONFIG')

logging.basicConfig(level=logging.INFO)

# @app.route('/')
# def runs():
#     if 'access_token' not in flask.session:
#         return flask.redirect(flask.url_for('login'))
#     client = stravalib.client.Client(access_token=flask.session['access_token'])
#     return flask.redirect(flask.url_for('runs.html'))



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
    #if form.raceDist.data[1]

    #flask.flash("raceDist",app.runList.raceDist[0])
    app.runList.filterList()
    return flask.redirect(flask.url_for('runs'))



@app.route('/')
@app.route('/runs', methods=['GET', 'POST'])
def runs():
    print "APP.RUNLIST",app.runList
    if 'access_token' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    if app.athlete is None:
        client = stravalib.client.Client(access_token=flask.session['access_token'])
        app.athlete = client.get_athlete()
    #runList=client.get_activities(limit=10)
    if app.runList is None:
        app.runList=RunUtils.RunList(client.get_activities(limit=defNRuns), raceDist="5k")
    form=RunsFilterForm(obj=app.runList)
    avgRiegel, avgCam=app.runList.avgTimeStrs()
    predString=flask.Markup("<h3>Average predictions for %s miles</h3>\n <h4>Riegel formula: %s</h4>\n <h4>Cameron formula %s</h4>\n"%(form.raceMi.data, avgRiegel, avgCam))
    print predString
    table=RunUtils.tableFromRunList(app.runList)
    #print "TABLE ",table.html

    return flask.render_template('runs.html', athlete=app.athlete, predString=predString, form=form, table=table)    

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
