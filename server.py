import requests
import json 
from flask import Flask, escape, request, url_for, render_template, redirect
import mysql.connector
from mysql.connector import errorcode
import time
from functools import partial
from datetime import datetime

app = Flask(__name__,)
global sql_connection

def connect_db(username, password, database):
    try:
        sql_connection = mysql.connector.connect(user=username,password=password,host="127.0.0.1",database=database)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Connection Error","You Username Or Password Is Incorrect")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Connection Error","Database doesn't exist")
        else:
            print("Connection Error",err)
    else:
        print("Connection Successful","Database Connected Successfully")
        return(sql_connection)

def validate_entry(vehicle_number,owner_name,owner_mobile):
    cursor = sql_connection.cursor()
    check_query = "SELECT * FROM Registrations WHERE vehicle_number = '%s';"
    cursor.execute(check_query,(vehicle_number))
    record = cursor.fetchall()
    if(record == []):
        addEntry_Both(cursor,vehicle_number,owner_name,owner_mobile)
        # else:
        #     tkinter.messagebox.showinfo("Info","This car is already registered in the database!")
        
    
def addEntry_Both(cursor,vehicle_number,owner_name,owner_mobile):
    insert_query_reg = "INSERT INTO Registrations VALUES (%s,%s,%s)"
    insert_query_entry = "INSERT INTO Entries VALUES (%s,%s,%s)"
    registration_table_data_tuple = (vehicle_number,owner_name,owner_mobile)
    vehicle_entries_data_tuple = (vehicle_number,datetime.now(),None)
    cursor.execute(insert_query_reg,registration_table_data_tuple)
    cursor.execute(insert_query_entry,vehicle_entries_data_tuple)
    sql_connection.commit()
    return


def allregistrations():
    cursor = sql_connection.cursor()
    check_query = "SELECT * FROM Registrations;"
    cursor.execute(check_query)
    record = cursor.fetchall()
    return(record)
        
def allentries():
    cursor = sql_connection.cursor()
    check_query = "SELECT * FROM Entries;"
    cursor.execute(check_query)
    record = cursor.fetchall()
    return(record)

@app.route('/')
def home():
    return render_template("home.html", name = "Shivam")

@app.route('/register', methods=["GET","POST"])
def register():
    print(sql_connection)
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        vehicle_number = request.form['vehicle_number']
        owner_name = request.form['owner_name']
        owner_mobile = request.form['owner_mobile']
    validate_entry(vehicle_number,owner_name,owner_mobile)
    return redirect(url_for('register'))

@app.route('/entry', methods=["GET","POST"])
def entry():
    if request.method == "GET":
        return render_template("entry.html")
    if request.method == "POST":
        vehicle_number = request.form['vehicle_number']
        owner_name = request.form['owner_name']
        owner_mobile = request.form['owner_mobile']
    validate_entry(vehicle_number,owner_name,owner_mobile)
    return redirect(url_for('register'))

@app.route('/registrations')
def registrations():
    all_registrations = allregistrations()
    return render_template("registrations.html", registrations = all_registrations)

@app.route('/entries')
def entries():
    all_entries = allentries()
    return render_template("entries.html", entries = all_entries)
     
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    sql_connection = connect_db("user","","Vehicle_Entry_System")
    app.run(debug='True', port=3000)
