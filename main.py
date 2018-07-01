from flask import Flask, render_template, request, send_file
import sqlite3 as sql
import base64
import os
app = Flask(__name__)

import sqlite3

conn = sqlite3.connect('Stu.db')


import base64
import csv

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, '/')


    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):        
        filename = file.filename        
        with open('People.csv') as csvfile:
              readCSV = csv.reader(csvfile, delimiter=',')

              for row in readCSV:
                name = row[0]
                grade =row[1]
                room =row[2]
                telnum =row[3]
                pic =row[4]
                keyword =row[5]
                with open(pic, "rb") as image_file:        
                  encoded_string = base64.b64encode(image_file.read()) 

                  dict = {pic:encoded_string.decode('utf-8')}

                
                con = sql.connect("Stu.db")
                cur = con.cursor()
                cur.execute("INSERT INTO UserEg (name,Grade,Room,Telnum,Pic,Keyword) VALUES (?,?,?,?,?,?)",(name,grade,room,telnum,dict[pic],keyword))
                con.commit()
        return render_template('home.html')
    
@app.route('/')
def home():
   return render_template('home.html')

@app.route('/list')
def list():
   con = sql.connect("Stu.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select * from UserEg")
   rows = cur.fetchall()

   return render_template("list.html",rows = rows)

@app.route('/DisplayGrade', methods=['POST'])
def DisplayGrade():
    DisplayGrade= request.form['DisplayGrade']
    con = sql.connect("Stu.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('SELECT name,Pic FROM UserEg where Grade < ?',(DisplayGrade,))
    rows = cur.fetchall()
    # return vehicleName
    return render_template('DisplayGrade.html', rows=rows)

@app.route('/SearchByName', methods=['POST'])
def SearchByName():
    SearchByName = request.form['SearchByName']
    con = sql.connect("Stu.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('SELECT Pic FROM UserEg where name like ? ', ('%'+SearchByName+'%',))
    rows = cur.fetchall()

    return render_template('SearchByName.html',rows=rows)

@app.route('/RemovePerson', methods=['POST'])
def RemovePerson():
    RemovePerson = request.form['RemovePerson']
    con = sql.connect("Stu.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('DELETE FROM UserEg where name = ? ', (RemovePerson,))
    con.commit()
    cur1 = con.cursor()
    cur1.execute('SELECT name FROM UserEg')
    rows = cur1.fetchall()

    return render_template('RemovePerson.html',rows=rows)

@app.route('/UpdateKeywords', methods=['POST'])
def UpdateKeywords():
    Name = request.form['Name']
    UpdateKeywords = request.form['UpdateKeywords']
    con = sql.connect("Stu.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('UPDATE UserEg SET Keyword = ? where name = ? ', (UpdateKeywords,Name,))
    con.commit()
    cur1 = con.cursor()
    cur1.execute('SELECT name,Keyword FROM UserEg')
    rows = cur1.fetchall()

    return render_template('UpdateKeywords.html',rows=rows)

@app.route('/UpdateGrades', methods=['POST'])
def UpdateGrades():
    UpdateGrades = request.form['UpdateGrades']
    Name = request.form['Name']
    con = sql.connect("Stu.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('UPDATE UserEg SET Grade = ? where name = ? ', (UpdateGrades,Name,))
    con.commit()
    cur1 = con.cursor()
    cur1.execute('SELECT name,Grade FROM UserEg1')
    rows = cur1.fetchall()

    return render_template('UpdateGrades.html',rows=rows)

@app.route('/ChangePicture', methods=['POST'])
def ChangePicture():
    ChangePicture = request.form['ChangePicture']
    target = os.path.join(APP_ROOT, '/')

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        filename = file.filename
        with open(filename, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            image=encoded_string.decode('utf-8')

    con = sql.connect("Stu.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('UPDATE UserEg SET Pic = ? WHERE name LIKE ?', (image,'%'+ChangePicture+'%'))
    con.commit()
    cur1 = con.cursor()
    cur1.execute('SELECT name,Pic FROM UserEg where name like ? ', ('%' + ChangePicture + '%',))

    rows = cur1.fetchall()

    return render_template('ChangePicture.html',rows=rows)



@app.route('/Question2')
def Question2():
    return render_template('SearchByName.html')
@app.route('/Question3')
def Question3():
    return render_template('DisplayGrade.html')
@app.route('/Question4')
def Question4():
    return render_template('ChangePicture.html')
@app.route('/Question5')
def Question5():
    return render_template('RemovePerson.html')
@app.route('/Question6')
def Question6():
    return render_template('UpdateKeywords.html')
@app.route('/Question7')
def Question7():
    return render_template('UpdateGrades.html')


if __name__ == '__main__':
   app.run(debug = True)