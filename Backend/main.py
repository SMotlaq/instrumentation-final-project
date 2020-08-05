from flask import Flask, request
from flask_cors import CORS, cross_origin
import DataBase as db
import datetime
import requests
import passwords

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#database     = r'D:\ac\Instrumentation\Final Ptoject\Backend\Main.db'
database     = r'C:\Users\Administrator\Desktop\instrumentation-final-project\Backend\Main.db'
conn         = db.create_connection(database)
mainPassword = passwords.mainPassword
db.create_table(conn)

#------------------------------ ESP requests ------------------------------#
@app.route('/test', methods = ['GET'])
def test():
    return 'ok'

@app.route('/get_status')
def get_status():
    password = request.args.get('password')
    response = ''
    if password==mainPassword:
        with conn:
            users = db.query_all_users(conn)
        for user in users:
            if user[5]=='1':
                response = response + user[4]
        return response
    else:
        return 'wrong password'

@app.route('/set_status')
#state
#10100001
def set_status():
    password = request.args.get('password')
    state    = request.args.get('state')
    if password==mainPassword:
        try:
            for number in range(len(state)):
                with conn:
                    db.update_parkings(conn, number+1, state[number])
            return 'ok'
        except Exception as e:
            print(e)
            return e
    else:
        return 'wrong password'

#----------------------------- Admin requests -----------------------------#
@app.route('/get_status2', methods = ['GET'])
def get_status2():
    password = request.args.get('password')
    response = ''
    if password==mainPassword:
        with conn:
            parkings = db.query_all_parkings(conn)
            if parkings!=0:
                for parking in parkings:
                    response = response + parking[1]

            users = db.query_all_users(conn)
            for user in users:
                if user[4]!='0':
                    temp = list(response)
                    temp[int(user[4])-1]='2'
                    response = "".join(temp)

        return response
    else:
        return 'wrong password'

@app.route('/addUser', methods = ['POST'])
#user_name, password_hashed, name
def addUser():
    password        = request.args.get('password')
    user_name       = request.args.get('user_name')
    password_hashed = request.args.get('password_hashed')
    name            = request.args.get('name')
    if password==mainPassword:
        try:
            with conn:
                print(user_name)
                print(password_hashed)
                print(name)
                print(db.add_user(conn, user_name, password_hashed, name))
            return 'ok'
        except Exception as e:
            print(e)
            return str(e)
    else:
        return 'wrong password'

@app.route('/parking_action', methods = ['POST'])
# password, user, address, action, value
def parking_action():
    password = request.args.get('password')
    address  = request.args.get('address')
    action   = request.args.get('action')
    value    = request.args.get('value')
    user     = request.args.get('user')
    print(password + '\n' + address + '\n' + action + '\n' + value + '\n' + user)
    if password==mainPassword:
        try:
            if action=='reserve':
                if value=='1':
                    with conn:
                        db.update_user(conn, user, parking_number = address)
                elif value=='0':
                    with conn:
                        db.update_user(conn, user, parking_number = '0')
            elif action=='control':
                if value=='1':
                    with conn:
                        db.update_user(conn, user, isClosed = '1')
                elif value=='0':
                    with conn:
                        db.update_user(conn, user, isClosed = '0')
            return 'ok'
        except Exception as e:
            print(e)
            return str(e)
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
    #app.run()
    app.run(host='176.9.199.181')
