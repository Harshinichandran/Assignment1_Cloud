from flask import Flask, render_template, request
import sqlite3 as sql
import base64
import os
app = Flask(__name__)

import sqlite3

conn = sqlite3.connect('Stu.db')
# print("Opened database successfully")
# conn.execute('CREATE TABLE UserEg (name TEXT, Grade VARCHAR, Room VARCHAR, Telnum VARCHAR, Pic VARCHAR, Keyword VARCHAR)')
# print("Table created successfully")

#-----------------------SQL CONNECTION--------------------------------
# print("Opened database successfully")
# conn.execute('CREATE TABLE UserDetails (name TEXT, Grade VARCHAR, Room VARCHAR, Telnum VARCHAR, Pic VARCHAR, Keyword VARCHAR)')
# print("Table created successfully")

# conn.execute("INSERT INTO stuDetails VALUES ('Nora','90','11','Nora.jpg','This is Nora')")
# conn.commit()
# conn.close()
#-------------------------------------------------------------------------

#-----------------------CSV FILE---------------------------------------------------
# import csv
# with open('People.csv') as csvfile:
#     readCSV = csv.reader(csvfile, delimiter=',')
#     names =[]
#     grades =[]
#     rooms =[]
#     telephones =[]
#     pictures =[]
#     keywords =[]
#     for row in readCSV:
#         name = row[0]
#         grade =row[1]
#         room =row[2]
#         telnum =row[3]
#         pic =row[4]
#         keyword =row[5]
#         print(name)
#         print(grade)
#         print(room)
#         print(telnum)
#         print(pic)
#         print(keyword)
#         conn.execute("INSERT INTO UserDetails (name,Grade,Room,Telnum,Pic,Keyword) VALUES (?,?,?,?,?,?)",(name,grade,room,telnum,pic,keyword))
#         conn.commit()
             
    #     names.append(name)
    #     grades.append(grade)
    #     rooms.append(room)
    #     telephones.append(telnum)
    #     pictures.append(pic)
    #     keywords.append(keyword)
    # print(names)
    # print(grades)
    # print(rooms)
    # print(telephones)
    # print(pictures)
    # print(keywords)
#------------------------------------------------------------------------------------------------------------------------------------------------

#---------------------------ENCODE IMAGE---------------------------------------------------------------------------------------------
# import base64
# with open("Abhishek.jpg", "rb") as image_file:
#       encoded_string = base64.b64encode(image_file.read())
#       print(encoded_string)
#----------------------------------------------------------------------------------------------------------------------------
import base64
import csv

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, '/')
    print('target')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):        
        filename = file.filename        
        with open('People.csv') as csvfile:
              readCSV = csv.reader(csvfile, delimiter=',')
              names =[]
              grades =[]
              rooms =[]
              telephones =[]
              pictures =[]
              keywords =[]
              for row in readCSV:
                name = row[0]
                grade =row[1]
                room =row[2]
                telnum =row[3]
                pic =row[4]
                keyword =row[5]
                # print(name)
                # print(grade)
                # print(room)
                # print(telnum)
                # print(pic)
                # print(keyword)
                with open(pic, "rb") as image_file:        
                  encoded_string = base64.b64encode(image_file.read())
                  # encoded_string.decode('utf-8')
                  # print(encoded_string.decode('utf-8'))
                  # print(encoded_string)
                dict = {pic: encoded_string.decode('utf-8')}
                # print (dict[pic])
                con = sql.connect("Stu.db")
                cur = con.cursor()
                cur.execute("INSERT INTO UserEg (name,Grade,Room,Telnum,Pic,Keyword) VALUES (?,?,?,?,?,?)",(name,grade,room,telnum,dict[pic],keyword))
                con.commit()
        return render_template('home.html')
    
@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def new_student():
   return render_template('student.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("Stu.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   # encoded_string=cur.execute("select pic from ")
   cur.execute("select * from UserEg")
   
   rows = cur.fetchall()

   return render_template("list.html",rows = rows)

# @app.route('/displayImage', methods=['POST'])
# def displayImage():
#     displayImage= request.form['displayImage'] 
#     con = sql.connect("Stu.db") 
#     con.row_factory = sql.Row
#     cur = con.cursor()
#     # print(vehicleName)
#     encoded_string = cur.execute('SELECT pic FROM UserDemo where name like \'%'+displayImage+'%\';')
#     with open(+displayImage+".png", "wb") as fh:
#       fh.write(base64.decodebytes(img_data))
#     # rows = cur.fetchall() 
#     # return vehicleName
#     return render_template('list.html', rows=rows)

if __name__ == '__main__':
   app.run(debug = True)