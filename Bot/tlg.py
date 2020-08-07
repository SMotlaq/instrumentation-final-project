import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import DataBase as db
import messages as ms
import buttons as bt
import requests
import hashlib
import datetime
import time
import signal
import tokens
import os

my_token = tokens.my_token

# server
database   = r'C:\Users\Administrator\Desktop\instrumentation-final-project\Bot\telegram.db'
# local:
#database   = r'D:\ac\Instrumentation\Final Ptoject\Bot\telegram.db'

log_chan   = -1001119482996
salman     = 95374546
conn       = db.create_connection(database)
bot        = telegram.Bot(token=my_token)
updater    = Updater(my_token)
db.create_table(conn)

def FSM(bot, update):
    inCome_uid, inCome_name, inCome_user_id = exctract_info(update.message.from_user)
    input_message = update.message.text
    current_state = ''
    with conn:
        query_result = db.query_user(conn, inCome_uid)
        print(query_result)
    if query_result!=0:
        current_state = query_result[8]
        print(current_state)
        if current_state == 'not signed home':
            if input_message == bt.home_not_signed[0][0]:   # vorood
                send_text(int(inCome_uid), ms.enter_user_name, bt.back)
                state = 'enter username sign in'
            else:
                send_text(int(inCome_uid), ms.han, bt.home_not_signed)
                state = 'not signed home'
        elif current_state== 'signed home':
            if input_message == bt.home_signed[0][0]:       # khorooj
                send_text(int(inCome_uid), ms.log_out_suc, bt.home_not_signed)
                state = 'not signed home'
            elif input_message == bt.home_signed[0][1]:     # reserve
                send_text(int(inCome_uid), ms.select_parking, bt.reserve)
                state = 'reserve'
            elif input_message == bt.home_signed[0][2]:     # ghofl
                if parking_available(inCome_uid):
                    send_text(int(inCome_uid), ms.ghofl_action, bt.lock)
                    state = 'lock'
                else:
                    send_text(int(inCome_uid), ms.no_parking, bt.home_signed)
                    state = 'signed home'
            else:
                send_text(int(inCome_uid), ms.han, bt.home_signed)
                state = 'signed home'
        elif current_state == 'enter username sign in':
            if input_message == bt.back[0][0]:              # back
                send_text(int(inCome_uid), ms.idle, bt.home_not_signed)
                state = 'not signed home'
            else:
                if user_name_isValid(inCome_uid, input_message):
                    temp_user = input_message
                    send_text(int(inCome_uid), ms.enter_password, bt.back)
                    state = 'enter password sign in'
                else:
                    send_text(int(inCome_uid), ms.wrong_user_name, bt.back)
                    state = 'enter username sign in'
        elif current_state == 'enter password sign in':
            if input_message == bt.back[0][0]:              # back
                send_text(int(inCome_uid), ms.enter_user_name, bt.back)
                state = 'enter username sign in'
            else:
                if password_isMatch(inCome_uid, input_message):
                    send_text(int(inCome_uid), ms.log_in_suc, bt.home_signed)
                    state = 'signed home'
                else:
                    send_text(int(inCome_uid), ms.match_error, bt.back)
                    state = 'enter password sign in'
        elif current_state == 'enter username sign up':
            if input_message == bt.back[0][0]:              # back
                send_text(int(inCome_uid), ms.idle, bt.home_not_signed)
                state = 'not signed home'
            else:
                if user_name_isFree(input_message):
                    send_text(int(inCome_uid), ms.enter_password, bt.back)
                    state = 'enter password sign up'
                else:
                    send_text(int(inCome_uid), ms.user_name_is_full, bt.back)
                    state = 'enter username sign up'
        elif current_state == 'enter password sign up':
            if input_message == bt.back[0][0]:              # back
                send_text(int(inCome_uid), ms.enter_user_name, bt.back)
                state = 'enter username sign up'
            else:
                set_password(inCome_uid, input_message)
                send_text(int(inCome_uid), ms.log_in_suc, bt.home_signed)
                state = 'signed home'
        elif current_state == 'lock':
            if input_message == bt.lock[1][0]:              # back
                send_text(int(inCome_uid), ms.idle, bt.home_signed)
                state = 'signed home'
            elif input_message == bt.lock[0][0]:            # close
                close_door(inCome_uid)
                send_text(int(inCome_uid), ms.close_sent, bt.home_signed)
                state = 'signed home'
            elif input_message == bt.lock[0][1]:            # open
                open_door(inCome_uid)
                send_text(int(inCome_uid), ms.open_sent, bt.home_signed)
                state = 'signed home'
            else:
                send_text(int(inCome_uid), ms.han, bt.home_signed)
                state = 'lock'
        elif current_state == 'reserve':
            if input_message == bt.reserve[1][0]:           # back
                send_text(int(inCome_uid), ms.idle, bt.home_signed)
                state = 'signed home'
            elif input_message == bt.reserve[0][0]:         # parking 1
                if reserve_parking(inCome_uid, '1'):
                    send_text(int(inCome_uid), ms.reserve_suc, bt.home_signed)
                    state = 'signed home'
                else:
                    send_text(int(inCome_uid), '', bt.reserve)
                    state = 'reserve'
            elif input_message == bt.reserve[0][1]:         # parking 2
                if reserve_parking(inCome_uid, '2'):
                    send_text(int(inCome_uid), ms.reserve_suc, bt.home_signed)
                    state = 'signed home'
                else:
                    send_text(int(inCome_uid), '', bt.reserve)
                    state = 'reserve'
            elif input_message == bt.reserve[0][2]:         # cancel
                if cancel_parking(inCome_uid):
                    send_text(int(inCome_uid), ms.cancel_suc, bt.home_signed)
                    state = 'signed home'
                else:
                    send_text(int(inCome_uid), '', bt.reserve)
                    state = 'reserve'
            else:
                send_text(int(inCome_uid), ms.han, bt.home_signed)
                state = 'reserve'
        # elif current_state == 'reserve action':
        #     if input_message == bt.reserve_action[1][0]:    # back
        #         pass
        #     elif input_message == bt.reserve_action[0][0]:  # cancel
        #         pass
        #     elif input_message == bt.reserve_action[0][1]:  # reserve kon
        #         pass
        #     else:
        #         pass
        db.update_user(conn, inCome_uid, state = state)
    else:
        reply_markup = telegram.ReplyKeyboardRemove()
        bot.send_message(chat_id = int(inCome_uid),text = ms.hit_start, reply_markup=reply_markup)
def start(bot, update):
    inCome_uid, inCome_name, inCome_user_id = exctract_info(update.message.from_user)
    try:
        with conn:
            isThere = db.query_user(conn, inCome_uid)
            if isThere==0:
                db.add_user(conn, inCome_uid, inCome_name, inCome_user_id, state = 'not signed home')
                if inCome_user_id=='None':
                    inCome_user_id = '[NO USER ID]'
                else:
                    inCome_user_id = '@' + inCome_user_id
                send_text(log_chan, ms.new_member_log + '\n' + inCome_user_id + '\n' + inCome_name)
                send_text(int(inCome_uid),ms.start,keyboard=bt.home_not_signed)
            else:
                db.update_user(conn, inCome_uid, name = inCome_name, user_id = inCome_user_id, state = 'not signed home')
                send_text(int(inCome_uid),ms.start,keyboard=bt.home_not_signed)
    except Exception as e:
        print(e)

def cancel_parking(inCome_uid):
    with conn:
        user = db.query_user(conn, inCome_uid)
    p_user_name, address = user[4], user[6]
    url = "http://176.9.199.181:5000/parking_action?password={}&user={}&address={}&action={}&value={}".format('dorosteaghaye', p_user_name, address, 'reserve', '0')
    response = requests.post(url)
    if response.status_code == 200:
        db.update_user(conn, inCome_uid, parking_number='0')
        return 1
    elif response.status_code == 403:
        send_text(int(inCome_uid),ms.reserve_not_allowed)
        return 0
def reserve_parking(inCome_uid, parking_number):
    try:
        with conn:
            user = db.query_user(conn, inCome_uid)
        p_user_name, address = user[4], user[6]
        url = "http://176.9.199.181:5000/get_status2?password={}".format('dorosteaghaye')
        response = requests.get(url).text
        if response[int(parking_number)-1]=='0':
            url = "http://176.9.199.181:5000/parking_action?password={}&user={}&address={}&action={}&value={}".format('dorosteaghaye', p_user_name, parking_number, 'reserve', '1')
            response = requests.post(url)
            print(response.text)
            db.update_user(conn, inCome_uid, parking_number=parking_number)
            return 1
        else:
            send_text(int(inCome_uid),ms.already_done)
            return 0
    except Exception as e:
        print(e)
        return 0
def open_door(inCome_uid):
    with conn:
        user = db.query_user(conn, inCome_uid)
    p_user_name, address = user[4], user[6]
    url = "http://176.9.199.181:5000/parking_action?password={}&user={}&address={}&action={}&value={}".format('dorosteaghaye', p_user_name, address, 'control', '0')

    response = requests.post(url)
    print(response)
def close_door(inCome_uid):
    with conn:
        user = db.query_user(conn, inCome_uid)
    p_user_name, address = user[4], user[6]
    url = "http://176.9.199.181:5000/parking_action?password={}&user={}&address={}&action={}&value={}".format('dorosteaghaye', p_user_name, address, 'control', '1')

    response = requests.post(url)
    print(response)
def set_password(inCome_uid, input_message):
    try:
        with conn:
            db.update_user(conn, inCome_uid, p_password = input_message)
            user = db.query_user(conn, inCome_uid)
        url = "http://176.9.199.181:5000/addUser?password=dorosteaghaye&user_name={}&password_hashed={}&name={}".format(user[4], input_message, user[2])
        response = requests.post(url)
        print(response.raw)
        return 1
    except Exception as e:
        print(e)
        return 0
def user_name_isFree(input_message):
    return 1
def password_isMatch(inCome_uid, input_message):
    try:
        with conn:
            user = db.query_user(conn, inCome_uid)
        if user!=0:
            url = "http://176.9.199.181:5000/login?password={}&user_name={}&password_hashed={}".format('dorosteaghaye', user[4], input_message)
            response = requests.post(url)
            if response.status_code == 200:
                db.update_user(conn, inCome_uid, p_password=input_message)
                return 1
            elif response.status_code == 403:
                send_text(int(inCome_uid),ms.match_error)
                return 0
        return 0
    except Exception as e:
        print(e)
def user_name_isValid(inCome_uid, input_message):
    try:
        with conn:
            db.update_user(conn, inCome_uid, p_user_name=input_message)
        return 1
    except Exception as e:
        print(e)
        return 0
def parking_available(inCome_uid):
    with conn:
        user = db.query_user(conn, inCome_uid)
        if user[6]!='0':
            return 1
        else:
            return 0

def exctract_info(chat_id):
    inCome_uid = str(chat_id['id'])
    inCome_user_id = chat_id['username']
    if inCome_user_id==None:
        inCome_user_id='None'
    first_name = chat_id['first_name']
    last_name = chat_id['last_name']
    if first_name==None:
        first_name = ''
    if last_name==None:
        last_name = ''
    else:
        last_name = ' ' + last_name
    inCome_name = first_name + last_name
    return inCome_uid, inCome_name, inCome_user_id
def send_photo(uid,msg,adrs):
    try:
        bot.sendChatAction(uid, 'UPLOAD_PHOTO')
        bot.sendPhoto(chat_id=uid, photo=open(adrs, 'rb'), caption=msg)
    except Exception as e:
        print(e)
def send_text(uid, msg, keyboard=None):
    try:
        bot.sendChatAction(uid, 'TYPING')
        if keyboard==None:
            bot.send_message(chat_id=uid, text=msg)
        else:
            reply_markup = telegram.ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
            bot.send_message(chat_id=uid, text=msg, reply_markup=reply_markup)
    except Exception as e:
        print(e)
def keyboard_handler(keyboard_buttons):
    return telegram.ReplyKeyboardMarkup(keyboard_buttons,resize_keyboard=True)
def handler(signum, frame):
    print('idle point')
    updater.idle()

signal.signal(signal.SIGINT, handler)
start_command = CommandHandler('start', start)
updater.dispatcher.add_handler(start_command)
state_handler = MessageHandler(Filters.text & (~Filters.command), FSM)
updater.dispatcher.add_handler(state_handler)
updater.start_polling()

send_text(salman, 'Bot started')

while True:
    clear = lambda: os.system('cls')
    # clear()
    # print('\n-- DONE --')
    time.sleep(5)
