from flask import Flask, request
import DataBase as db
import tlg
import datetime
import requests
import passwords

app          = Flask(__name__)
database     = r'D:\ac\Instrumentation\Final Ptoject\Backend\Main.db'
conn         = db.create_connection(database)
mainPassword = password.mainPassword
db.create_table(conn)

#------------------------------ESP requests------------------------------#
@app.route('/fac/status', methods = ['GET'])
def whatsup():
    password = request.args.get('password')
    if password==mainPassword:
        global global_state
        foo  = global_state
        global_state = '0'
        return foo
    else:
        return 'wrong password'

@app.route('/fac/authen', methods = ['POST'])
def authenticate():
    password = request.args.get('password')
    if password==mainPassword:
        global conn
        response = '0'
        currentDT = datetime.datetime.now()
        day_corrected = ['3','4','5','6','7','1','2']
        cardID = request.args.get('cardID')
        PIR    = request.args.get('PIR')
        id = db.query(conn, 'SELECT id FROM members WHERE cardID=?', (cardID,))
        if id==[]:
            response = '0 - id reject'
        else:
            groups = db.query(conn, 'SELECT group_id FROM permissions WHERE std_id=?', (id[0][0],))
            if groups==[]:
                return '404 - no permission defined for this user :('
            for group in groups:
                times = db.query(conn, 'SELECT from_,to_,day FROM groups WHERE id=?', (group[0][0],))
                from_, to_, day_ = datetime.datetime.strptime(times[0][0],"%H:%M:%S").time(), datetime.datetime.strptime(times[0][1],"%H:%M:%S").time(), times[0][2]
                if day_corrected[currentDT.weekday()] not in day_:
                    response = '0 - day reject'
                elif from_<currentDT.time() and to_>currentDT.time():
                    response = '1'
                    log(conn, cardID, response, PIR)
                    return '1'
                else:
                    response = '0 - time reject'
        log(conn, cardID, response, PIR)
        return response
    else:
        return 'wrong password'

@app.route('/fac/addUser', methods = ['POST'])
def addUser():
    global conn
    cardID   = request.args.get('cardID')
    stdNum   = request.args.get('stdNum')
    password = request.args.get('password')
    if password==mainPassword:
        with conn:
            db.update_cardID(conn, stdNum, cardID,)
        return 'added'
    else:
        return 'wrong password'

#-----------------------------Admin requests-----------------------------#
@app.route('/fac/new', methods = ['POST'])
def newMember():
    password = request.args.get('password')
    if password==mainPassword:
        global conn
        global global_state
        stdNum = request.args.get('stdNum')
        name   = request.args.get('name')
        family = request.args.get('family')
        groups = request.args.get('groups')
        isGirl = request.args.get('isGirl')
        with conn:
            id_ = db.add_member(conn, (stdNum, 'Null', name, family, isGirl,))
            for group in groups:
                db.add_permission(conn, (id_, group,))
        global_state = str(stdNum)
        return 'wating for cardID'
    else:
        return 'wrong password'

@app.route('/fac/config/groups', methods = ['POST'])
def groups():
    password = request.args.get('password')
    if password==mainPassword:
        global conn
        raw_data = request.get_json()
        if raw_data['add']!={}:
            with conn:
                db.add_group(conn, (raw_data['add']['name'], raw_data['add']['from'],
                                    raw_data['add']['to'], raw_data['add']['days'],))
        if raw_data['remove']!={}:
            with conn:
                db.delete_group(conn, raw_data['remove'])
        if raw_data['edit']!={}:
            with conn:
                if raw_data['edit']['name']!='Null':
                    db.update_groups(conn, 'UPDATE groups SET groupName=? WHERE id=?', (raw_data['edit']['name'],raw_data['edit']['id'],))
                if raw_data['edit']['from']!='Null':
                    db.update_groups(conn, 'UPDATE groups SET from_=? WHERE id=?', (raw_data['edit']['from'],raw_data['edit']['id'],))
                if raw_data['edit']['to']!='Null':
                    db.update_groups(conn, 'UPDATE groups SET to_=? WHERE id=?', (raw_data['edit']['to'],raw_data['edit']['id'],))
                if raw_data['edit']['days']!='Null':
                    db.update_groups(conn, 'UPDATE groups SET day=? WHERE id=?', (raw_data['edit']['days'],raw_data['edit']['id'],))
        return 'Done'
    else:
        return 'wrong password'

@app.route('/fac/config/members', methods = ['POST'])
def members():
    password = request.args.get('password')
    if password==mainPassword:
        global conn
        raw_data = request.get_json()
        if raw_data['remove']!={}:
            with conn:
                db.delete_member(conn, stdNum = raw_data['remove'])
        return 'Done'
    else:
        return 'wrong password'

@app.route('/fac/config/permissions', methods = ['POST'])
def permissions():
    password = request.args.get('password')
    if password==mainPassword:
        global conn
        raw_data = request.get_json()
        if raw_data['add']!={}:
            with conn:
                db.add_permission(conn, raw_data['add']['stdNum'], raw_data['add']['groupID'])
        if raw_data['remove']!={}:
            with conn:
                db.delete_permission(conn, raw_data['remove']['stdNum'], raw_data['remove']['groupID'])
        return 'Done'
    else:
        return 'wrong password'

@app.route('/fac/config/open', methods = ['POST'])
def open():
    password = request.args.get('password')
    if password==mainPassword:
        global global_state
        global_state = '1'
        return 'command sent'
    else:
        return 'wrong password'


def log(conn, cardID, response, session):
    currentDT = datetime.datetime.now().weekday()
    day_corrected = ['3','4','5','6','7','1','2']
    time = requests.get("http://gahshomar-api.herokuapp.com/zone/Asia-Tehran").text.replace(' ','').split(',')[0]
    date = requests.get("http://gahshomar-api.herokuapp.com/date/jalali"     ).text.replace(' ','')
    time, date = cleaner(time, date)
    if response == '0 - id reject':
        tlg.send('⚠️ Unsuccessful attempt (unknown card) ⚠️\n💳 Unique ID: ' + cardID + '\n🕗  ' + time + '\n🗓  ' + date)
        with conn:
            db.add_log(conn, ('Null',cardID, 'Null', 'Null', date, time, session, 'failed',))
        return 0
    if response == '1':
        status = 'granted'
    else:
        status = 'failed'
    member = db.query(conn,'SELECT stdNum, name, family, isGirl FROM members WHERE cardID=?', (cardID,))
    with conn:
        db.add_log(conn, (member[0][0], cardID, member[0][1], member[0][2], date, time, session, status,))
    name   = member[0][1]
    family = member[0][2]
    gender_icon  = {1:'🙍🏻‍♀️‍ ',
                    0:'🙍🏻‍♂️ '}
    status_text  = {'granted':'✅ Granted  \n',
                    'failed' :'❌ Rejected \n'}
    weekday_name = {'1':'شنبه',
                    '2':'یکشنبه',
                    '3':'دوشنبه',
                    '4':'سه شنبه',
                    '5':'چهارشنبه',
                    '6':'پنجشنبه',
                    '7':'جمعه'}
    tlg.send(status_text[status] + gender_icon[member[0][3]] + name + ' ' + family + '\n🕗  ' + time + '\n🗓  ' + date + '\n  ' + weekday_name[day_corrected[currentDT]])
    return 0

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

if __name__ == '__main__':
    app.run(host='178.63.211.120')
