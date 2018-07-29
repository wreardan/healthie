from flask import Flask
from flask import request
import flask
import requests
import time
from datetime import datetime
import json
import hashlib
from flask import Response, stream_with_context, redirect, flash, render_template, session, abort
import boto3, botocore

import os
import time

if 'DB_PASSWORD' in os.environ:
    import MySQLdb as mdb
    db_password = os.environ['DB_PASSWORD']
    con = mdb.connect("localhost","root",db_password,"healthie")


    S3_BUCKET = 'healthie.us2'  # app.config["S3_BUCKET"]
    s3 = boto3.client('s3', aws_access_key_id=os.environ["AWS_KEY"], aws_secret_access_key=os.environ["AWS_SECRET"])

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
            session['user_id'] = user_id

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


@app.route('/logout', methods = ['GET'])
def logout():
    session['user_id'] = 0

    return redirect('/')



@app.route('/records', methods = ['GET', 'POST'])
def records():
    if not 'user_id' in session or not (int(session['user_id']) > 0):
        return redirect('/login')
    """record_list = [
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
    ]"""
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Record WHERE user_id='%d'" % session["user_id"])
        record_list = cur.fetchall()
    return render_template('records.html', record_list=record_list)


@app.route('/schedule', methods = ['GET', 'POST'])
def schedule():
    # if not 'user_id' in session or not (int(session['user_id']) > 0):
    #     return redirect('/login')
    return render_template('schedule.html')


@app.route('/fitbit', methods = ['GET', 'POST'])
def fitbit():
    if not 'user_id' in session or not (int(session['user_id']) > 0):
        return redirect('/login')
    return render_template('fitbit.html')



@app.route('/fitbitredirect', methods = ['GET', 'POST'])
def fitbitredirect():
    return ""


@app.route('/googleredirect', methods = ['GET', 'POST'])
def googleredirect():
    print("received google redirect")
    return ""



@app.route('/communicate', methods = ['GET', 'POST'])
def communicate():
    if not 'user_id' in session or not (int(session['user_id']) > 0):
        return redirect('/login')
    return render_template('communicate.html')


@app.route('/fitbit', methods = ['GET', 'POST'])
def fitbit():
    if not 'user_id' in session or not (int(session['user_id']) > 0):
        return redirect('/login')
    return render_template('fitbit.html')


# http://zabana.me/notes/upload-files-amazon-s3-flask.html
@app.route("/attachment", methods = ['POST'])
def attachment():
    if request.method == 'POST':
        if "attachment" not in request.files:
            return "No attachment in request: " + json.dumps(request.files)

        file = request.files["attachment"]
        file.filename = secure_filename(file.filename)
        url = upload_file_to_s3(file, S3_BUCKET, 'private')

        with con:

            cur = con.cursor()
            upload_date = time.strftime('%Y-%m-%d %H:%M:%S')
            uploaded_by = "San Francisco General"
            user_id = session['user_id']
            cur.execute("INSERT INTO Record(filename, upload_date, uploaded_by, user_id, url) VALUES('%s', '%s', '%s', %d, '%s');" %
                (file.filename, upload_date, uploaded_by, user_id, url))
            attachment_id = cur.lastrowid
            return url


#from werkzeug.security import secure_filename
# HACK HACK HACK
def secure_filename(filename):
    return filename

# http://zabana.me/notes/upload-files-amazon-s3-flask.html
# https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html
# http://boto3.readthedocs.io/en/latest/guide/s3.html
def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket_name,
                'Key': file.filename
            }
        )
        return url

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Exception during S3 upload: ", e)
        return e


if __name__ == "__main__":
    # https://stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session
    kwargs = {}
    if 'SESSION_SECRET' in os.environ:
        app.secret_key = os.environ['SESSION_SECRET']
        kwargs = {"ssl_context": ('../cert.pem', '../privkey.pem')}
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host= '0.0.0.0', **kwargs)
