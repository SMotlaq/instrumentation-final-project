from flask import Flask, request
import DataBase as db
import datetime
import requests
import passwords

app          = Flask(__name__)
database     = r'D:\ac\Instrumentation\Final Ptoject\Backend\Main.db'
conn         = db.create_connection(database)
mainPassword = password.mainPassword
db.create_table(conn)

#------------------------------ ESP requests ------------------------------#
@app.route('/get_status', methods = ['GET'])
def get_status():
    password = request.args.get('password')
    if password==mainPassword:
        return None
    else:
        return 'wrong password'

@app.route('/set_status', methods = ['POST'])
def set_status():
    password = request.args.get('password')
    if password==mainPassword:
        return None
    else:
        return 'wrong password'

#----------------------------- Admin requests -----------------------------#
@app.route('/addUser', methods = ['POST'])
#user_name, password_hashed, name
def addUser():
    password = request.args.get('password')
    if password==mainPassword:
        return None
    else:
        return 'wrong password'

@app.route('/parking_action', methods = ['POST'])
# password, address, action
def parking_action():
    password = request.args.get('password')
    if password==mainPassword:
        return None
    else:
        return 'wrong password'

def cleaner(time, date):
    time_elements = time.split(':')
    date_elements = date.split('/')
    if len(time_elements[0])==1:
        time_elements[0] = '0' + time_elements[0]
    if len(time_elements[1])==1:
        time_elements[1] = '0' + time_elements[1]
    if len(time_elements[2])==1:
        time_elements[2] = '0' + time_elements[2]
    if len(date_elements[0])==1:
        date_elements[0] = '0' + date_elements[0]
    if len(date_elements[1])==1:
        date_elements[1] = '0' + date_elements[1]
    if len(date_elements[2])==1:
        date_elements[2] = '0' + date_elements[2]
    newTime = time_elements[0]+':'+time_elements[1]+':'+time_elements[2]
    newDate = date_elements[2]+'/'+date_elements[1]+'/'+date_elements[0]
    return newTime, newDate
def getTime():
    time = requests.get("http://gahshomar-api.herokuapp.com/zone/Asia-Tehran").text.replace(' ','').split(',')[0]
    date = requests.get("http://gahshomar-api.herokuapp.com/date/jalali"     ).text.replace(' ','')
    time, date = cleaner(time, date)
    return time, date

if __name__ == '__main__':
    app.run()#host='178.63.211.120')
