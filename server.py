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

def find_time(t):
    return(str(t.time())[0:5])

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
    in_time = find_time(datetime.now())
    registration_table_data_tuple = (vehicle_number,owner_name,owner_mobile)
    vehicle_entries_data_tuple = (vehicle_number,in_time,None)
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

def search_entry(vehicle_number):
    cursor = sql_connection.cursor()
    check_query = "SELECT * FROM Entries WHERE out_time IS NULL and vehicle_registration_number = '"+vehicle_number+"';"
    cursor.execute(check_query)
    record = cursor.fetchall()
    if(record == []):
        return(record)
    else:
        for row in record:
            data = {
                "vehicle_registration_number": row[0],
                "in_time": row[1]
            }
        return (data)

def close_entry(vehicle_entry_number):
    cursor = sql_connection.cursor()
    out_time = find_time(datetime.now())
    mod_query =  "UPDATE Entries SET out_time = %s WHERE vehicle_registration_number = %s AND out_time IS NULL"
    cursor.execute(mod_query,(out_time, vehicle_entry_number))
    sql_connection.commit()
    return

def add_entry(vehicle_entry_number):
    cursor = sql_connection.cursor()
    insert_query_two = "INSERT INTO Entries VALUES (%s,%s,%s)"
    in_time = find_time(datetime.now())
    vehicle_entries_data_tuple = (vehicle_entry_number,in_time,None)
    cursor.execute(insert_query_two,vehicle_entries_data_tuple)
    sql_connection.commit()
    return

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", name = "Shivam")

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        vehicle_number = request.form['vehicle_number']
        owner_name = request.form['owner_name']
        owner_mobile = request.form['owner_mobile']
    validate_entry(vehicle_number,owner_name,owner_mobile)
    return redirect(url_for('home'))

@app.route('/entry', methods=["GET","POST"])
def entry(): 
    if request.method == "GET":
        search_result = request.args.get('search_result')
        search_vehicle_entry_number = request.args.get('search_vehicle_entry_number')
        if(request.args.get('in_time')):
            in_time = request.args.get('in_time')
            return render_template("entry.html", vehicle_entry_number = search_vehicle_entry_number, in_time = in_time, out_time = find_time(datetime.now()),check = 1)
        else:
            return render_template("entry.html", vehicle_entry_number=search_vehicle_entry_number, in_time = find_time(datetime.now()), check = 0)
    if request.method == "POST":
        vehicle_entry_number = request.form['vehicle_entry_number']
        if 'out_time' not in request.form:
            add_entry(vehicle_entry_number)
        else:
            close_entry(vehicle_entry_number)
        return redirect(url_for('home'))




@app.route('/registrations')
def registrations():
    all_registrations = allregistrations()
    return render_template("registrations.html", registrations = all_registrations)

@app.route('/entries')
def entries():
    all_entries = allentries()
    return render_template("entries.html", entries = all_entries)

@app.route('/search', methods=["GET","POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    if request.method == "POST":
        search_vehicle_entry_number = request.form['search_vehicle_entry_number']
        search_result = search_entry(search_vehicle_entry_number)
        if(search_result == []):
            return redirect(url_for('entry', search_vehicle_entry_number = search_vehicle_entry_number))
        else:
            return redirect(url_for('entry', in_time = search_result["in_time"], search_vehicle_entry_number = search_vehicle_entry_number))
     
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    sql_connection = connect_db("user","","Vehicle_Entry_System")
    app.run(debug='True', port=3000)
