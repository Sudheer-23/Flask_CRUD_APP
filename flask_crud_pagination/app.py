from flask import Flask, render_template, request, url_for, redirect, flash, get_flashed_messages
from flaskext.mysql import MySQL
from numpy import roll
import pymysql

app = Flask(__name__)
app.secret_key = "Sudheer"

mysql = MySQL()

# MySQL Configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'sudheer123'
app.config['MYSQL_DATABASE_DB'] = 'college'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def home():
    con = mysql.connect()
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM students;')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', student = data)


@app.route('/add_student',methods=['POST'])
def add_student():
    con = mysql.connect()
    cur = con.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        id = request.form['id']
        roll = request.form['Roll']
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur.execute('INSERT INTO students(id,name,roll,mobile,email) VALUES(%s,%s,%s,%s,%s);',(id,fullname,roll,phone,email))
        con.commit()
        flash('Data Added Successfully')
        return redirect(url_for('home'))


@app.route('/edit/<id>',methods=['GET','POST'])
def get_contact(id):
    con = mysql.connect()
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM students WHERE id = %s',(id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html',student = data[0])


@app.route('/update/<id>',methods=['GET','POST'])
def update_contact(id):
    con = mysql.connect()
    cur = con.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        roll = request.form['Roll']
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur.execute('UPDATE students SET name = %s,roll = %s,mobile = %s,email = %s WHERE id = %s;',(fullname,roll,phone,email,id))
        con.commit()
        flash('Data Updated Successfully')
        return redirect(url_for('home'))
   

@app.route('/delete/<string:id>',methods=['GET','POST'])
def delete_contact(id):
    con = mysql.connect()
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute('DELETE FROM students WHERE id = {};'.format(id))
    con.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('home'))

@app.route('/greet')
def greet():
    return render_template('layout.html')

if __name__ == '__main__':
    app.run(debug=True)