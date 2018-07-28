from flask import Flask
from flask import request
import flask
import time
from datetime import datetime
import json
import hashlib
from flask import Response, stream_with_context, redirect, flash, render_template, session, abort
import boto3, botocore

app = Flask(__name__)
app.debug = True

@app.route('/', defaults={'path': ''}, methods = ['PUT', 'GET'])
@app.route('/<path:path>', methods = ['PUT', 'GET'])
def home(path):
    if not 'user_id' in session or not (int(session['user_id']) > 0):
        return redirect('/login')
    return render_template('home.html')



@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user_id = db.get('Username:' + username)

        if user_id == '' or user_id is None:
            return render_template('login.html')
        if password_hash != db_password_hash:
            return render_template('login.html')

        session['user_id'] = user_id

        return redirect('/')


@app.route('/records', methods = ['GET', 'POST'])
def records():
    return render_template('records.html')


@app.route('/communicate', methods = ['GET', 'POST'])
def communicate():
    return render_template('communicate.html')



if __name__ == "__main__":
    # https://stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session
    #app.secret_key = 'Yarwarl'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(host= '0.0.0.0')

