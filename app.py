from flask import Flask
from flask import request
import flask
import time
from datetime import datetime
import json
import hashlib
from flask import Response, stream_with_context, redirect, flash, render_template, session, abort
import boto3, botocore
import MySQLdb as mdb
import os
import time

db_password = os.environ['DB_PASSWORD']
con = mdb.connect("localhost","root",db_password,"healthie")

app = Flask(__name__)
app.debug = True

@app.route('/', defaults={'path': ''}, methods = ['PUT', 'GET'])
@app.route('/<path:path>', methods = ['PUT', 'GET'])
def home(path):
    #if not 'user_id' in session or not (int(session['user_id']) > 0):
        #return redirect('/login')
    return render_template('index.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        phone = int(request.form.get('phone'))
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = int(request.form.get('zipcode'))
        password = request.form.get('password')
        password2 = request.form.get('password2')

        assert(password == password2)
        password_hash = hash_password(password)

        # Hook up Trulioo here

        # Insert patient into database
        with con:
            
            cur = con.cursor()
            reg_date = time.strftime('%Y-%m-%d %H:%M:%S')
            cur.execute("INSERT INTO User(firstname, lastname, email, password_hash, phone, address, city, state, zipcode, reg_date) VALUES('%s', '%s', '%s', '%s', %d, '%s', '%s', '%s', %d, '%s');" % 
                (firstname, lastname, email, password_hash, phone, address, city, state, zipcode, reg_date))

            user_id = cur.lastrowid
            session['user_id'] = uesr_id

        return redirect('/records')

    else:
        return render_template('register.html')

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_hash = hash_password(password)
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT * FROM User WHERE email='%s'" % username)
            rows = cur.fetchall()
            if len(rows) == 0:
                return render_template('login.html')
            user = rows[0]
            db_password_hash = user['password_hash']
            user_id = user['id']

        if user_id == '' or user_id is None:
            return render_template('login.html')
        if password_hash != db_password_hash:
            return render_template('login.html')

        session['user_id'] = user_id

        return redirect('/records')

    else:
        return render_template('login.html')


@app.route('/records', methods = ['GET', 'POST'])
def records():
    if not 'user_id' in session or not (int(session['user_id']) > 0):
        return redirect('/login')
    record_list = [
        {
            "filename": "Chest X-Ray",
            "date": "4/17/17",
            "author": "Fairview Health Services",
        },
        {
            "filename": "Chest X-Ray",
            "date": "4/18/17",
            "author": "Fairview Health Services",
        },
        {
            "filename": "Abdominal Ultrasound",
            "date": "4/19/17",
            "author": "Fairview Health Services",
        },
    ]
    return render_template('records.html', record_list=record_list)


@app.route('/schedule', methods = ['GET', 'POST'])
def schedule():
    if not 'user_id' in session or not (int(session['user_id']) > 0):
        return redirect('/login')
    return render_template('schedule.html')


@app.route('/fitbit', methods = ['GET', 'POST'])
def fitbit():
    if not 'user_id' in session or not (int(session['user_id']) > 0):
        return redirect('/login')
    return render_template('fitbit.html')



@app.route('/fitbitredirect', methods = ['GET', 'POST'])
def fitbitredirect():
    return ""



@app.route('/communicate', methods = ['GET', 'POST'])
def communicate():
    if not 'user_id' in session or not (int(session['user_id']) > 0):
        return redirect('/login')
    return render_template('communicate.html')



if __name__ == "__main__":
    # https://stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session
    app.secret_key = os.environ['SESSION_SECRET']
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(host= '0.0.0.0')

