import os
import time
import requests
from flask import Flask
from threading import Thread
import logging
from pyrogram import Client, idle
import DATA.common_globals as cg
from COM.now_is import now_is
from FUSI.AutoRecHandler import AutoRecHandler


PATH = os.getcwd()


bot = Client("fusi-render",
             api_id=24327835,
             api_hash='d50ef0a4d30eea70af1c5e74009c333f',
             bot_token='6464549272:AAEwtgVEAFTTgAm1ti1CsI_oKHHOxkmTFp4',
             max_concurrent_transmissions=4)

try:
    bot.start()
except ConnectionError:
    pass

app = Flask('')
# logging.getLogger('werkzeug').disabled = True


@app.route('/')
def index():
    return "Web App is alive!"


@app.route('/start')
def start():
    url = cg.lives_url
    querystring = {
        "lang": "1",
        "os": "h5",
        "cid": "ftsH5",
        "webVersion": "1000",
        "uid": cg.user_uid,
        "token": cg.user_token,
        "pageNum": "1",
        "pageSize": "99",  # what max ?
        "pass": "true",
        "pageID": cg.page_id
    }
    headers = {"referer": cg.referer}

    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()

        print(f'{now_is()} - {cg.YELLOW}check{cg.RESET}')

        if data['code'] == 1:
            for room in data['rooms']:
                name = room['nickname']
                state = room['liveState']  # 0 offline / 1 live
                uid = room['uid']
                title = room['introduce']

                live_data = {'uid': uid,
                             'name': name,
                             'title': title}

                if state > 0:
                    if uid not in cg.current_records:
                        cg.current_records.add(uid)
                        AutoRecHandler(bot, PATH, uid, live_data).start()
            time.sleep(cg.refresh_freq)

        elif data['code'] == -1000:
            bot.send_message(cg.errors, 'Token expired')
            bot.send_message(cg.admin, 'Token expired')
            print(f'{now_is()} - Token expired\n')

        else:
            bot.send_message(cg.errors, f'Unhandled response : {data}')
            print(f'{now_is()} - Unhandled response while checking lives: {data}\n')

    except Exception as e:
        bot.send_message(cg.errors, f'Error while checking lives : {e}')
        print(f'{now_is()} - Error while checking lives : {e}\n')

    requests.request("GET", 'http://127.0.0.1:8080/start')       # os.environ['SELF_URL']
    return "BOT not working"


def app_run():
    app.run(host="0.0.0.0", port=8080)


def start_server():
    server = Thread(target=app_run)
    server.name = 'SERVER'
    server.start()
    bot_idle = Thread(target=idle())
    bot_idle.name = 'BOT IDLE'
    bot_idle.start()


start_server()
