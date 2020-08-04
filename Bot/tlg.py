import requests
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import time
import datetime
import DataBase as db
import signal
import messages as ms
import buttons as bt
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
    if query_result!=0 and query_result!='Fail':
        current_state = query_user[8]
        if current_state == 'not signed home':
            if input_message == bt.home_not_signed[0][0]:   # vorood
                pass
            elif input_message == bt.home_not_signed[0][1]:  # sabte nam
                pass
            else:
                pass
        elif current_state== 'signed home':
            if input_message == bt.home_signed[0][0]:       # khorooj
                pass
            elif input_message == bt.home_signed[0][1]:     # reserve
                pass
            elif input_message == bt.home_signed[0][2]:     # ghofl
                pass
            else:
                pass
        elif current_state == 'enter username sign in':
            if input_message == bt.back[0][0]:              # back
                pass
            else:
                pass
        elif current_state == 'enter password sign in':
            if input_message == bt.back[0][0]:              # back
                pass
            else:
                pass
        elif current_state == 'enter username sign up':
            if input_message == bt.back[0][0]:              # back
                pass
            else:
                pass
        elif current_state == 'enter password sign up':
            if input_message == bt.back[0][0]:              # back
                pass
            else:
                pass
        elif current_state == 'lock':
            if input_message == bt.lock[1][0]:              # back
                pass
            elif input_message == bt.lock[0][0]:            # close
                pass
            elif input_message == bt.lock[0][1]:            # open
                pass
            else:
                pass
        elif current_state == 'reserve':
            if input_message == bt.reserve[1][0]:           # back
                pass
            elif input_message == bt.reserve[0][0]:         # parking 1
                pass
            elif input_message == bt.reserve[0][1]:         # parking 2
                pass
            else:
                pass
        elif current_state == 'reserve action':
            if input_message == bt.reserve_action[1][0]:    # back
                pass
            elif input_message == bt.reserve_action[0][0]:  # cancel
                pass
            elif input_message == bt.reserve_action[0][1]:  # reserve kon
                pass
            else:
                pass
    else:
        reply_markup = telegram.ReplyKeyboardRemove()
        bot.send_message(chat_id = int(inCome_uid),text = ms.hit_start, reply_markup=reply_markup)
def start(bot, update):
    inCome_uid, inCome_name, inCome_user_id = exctract_info(update.message.from_user)
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
            db.edit_user(conn, inCome_uid, name = inCome_name, user_id = inCome_user_id, state = 'signed home')
            send_text(int(inCome_uid),ms.start,keyboard=bt.home_not_signed)

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
    clear()
    print('\n-- DONE --')
    time.sleep(5)
