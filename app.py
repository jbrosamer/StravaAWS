#!/usr/bin/python

import flask
import logging
import stravalib
import os
import RunUtils

app = flask.Flask(__name__)
if os.environ.get('FIXSTRAVA_CONFIG') is None:
    os.environ['FIXSTRAVA_CONFIG']='settings.txt'
app.config.from_envvar('FIXSTRAVA_CONFIG')
# app.config['SECRET_KEY'] = 'cC1YCIWOj9GgWspgNEo2'
# app.config['CLIENT_SECRET'] = '85a5f1be79a97e5fe19b99d12fa2196c81da4629'
# app.config['CLIENT_ID'] = '7582'

logging.basicConfig(level=logging.INFO)

@app.route('/')
def homepage():
    if 'access_token' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    return flask.redirect(flask.url_for('prediction'))

@app.route('/login')
def login():
    client = stravalib.client.Client()
    auth_url = client.authorization_url(client_id=app.config['CLIENT_ID'],
            scope='write',
            redirect_uri='http://127.0.0.1:7123/auth')
    return flask.render_template('login.html', auth_url=auth_url)

@app.route('/logout')
def logout():
    flask.session.pop('access_token')
    return flask.redirect(flask.url_for('homepage'))

@app.route('/update')
def update():
    return flask.render_template('update.html')

@app.route('/prediction')
def prediction():
    if 'access_token' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    client = stravalib.client.Client(access_token=flask.session['access_token'])
    athlete = client.get_athlete()
    runList=client.get_activities(limit=10)
    app.runList=runList
    table=Runs.runsToTable(runList)
    return flask.render_template('prediction.html', athlete=athlete, table=table)



    

@app.route('/auth')
def auth_done():
    # TODO: check for errors 
    code = flask.request.args.get('code', '')
    client = stravalib.client.Client()
    token = client.exchange_code_for_token(client_id=app.config['CLIENT_ID'],
            client_secret=app.config['CLIENT_SECRET'],
            code = code)
    flask.session['access_token'] = token
    return flask.redirect(flask.url_for('homepage'))

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
