from flask import Flask, render_template, Response, request, session, redirect, flash
from flask.helpers import flash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
# from flask_mysqldb import MySQL
import mysql.connector

db = mysql.connector.connect(host='localhost',user='root',passwd='12345678')
cur = db.cursor()

app = Flask(__name__)

app.secret_key = 'secret key :)'

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    flag = None
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        pswd = request.form.get('pswd')
        cur.execute("SELECT * FROM python.user_info WHERE user_id = %s AND pswd = %s", (user_id, pswd))
        row = cur.fetchone()
        if row is not None:
            mobile_number = row[1]
            # session['logedin'] = True
            # session['user_id'] = user_id
            return render_template('after_login.html', user_id = user_id, mobile_number = mobile_number)
        else:
            flag = 'Not None'
            return render_template('login.html', flag = flag)

    return render_template('login.html', flag = flag)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        mobile_number = request.form.get('mobile_number')
        pswd = request.form.get('pswd')
        # print(user_id, password, mobile_number)
        cur.execute("INSERT INTO python.user_info VALUES (%s, %s, %s)", (user_id, pswd, mobile_number))
        db.commit()
        # cur.close()
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)