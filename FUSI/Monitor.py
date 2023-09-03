from threading import Thread
import time
import requests
import DATA.common_globals as cg
from FUSI.AutoRecHandler import AutoRecHandler
from COM.now_is import now_is


class Monitor(Thread):
    def __init__(self, bot, path) -> None:
        Thread.__init__(self)
        self.bot = bot
        self.path = path
        self.name = 'MONITOR'
        self.url = "https://cpapi.footseen.xyz/room/queryUserLikeList"
        self.querystring = {
            "lang": "1",
            "os": "h5",
            "cid": "ftsH5",
            "webVersion": "1000",
            "uid": cg.user_uid,
            "token": cg.user_token,
            "pageNum": "1",
            "pageSize": "99",  # what max ?
            "pass": "true",
            "pageID": "56f901109e787c055c5ca8bd872fe88b"
        }
        self.headers = {"referer": "https://www.footseen.xyz/"}
        self.stop = False

    def run(self) -> None:
        while not self.stop:
            try:
                response = requests.request("GET", self.url, headers=self.headers, params=self.querystring)
                data = response.json()

                # print(len(data['rooms']))

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
                                AutoRecHandler(self.bot, self.path, uid, live_data).start()
                    time.sleep(cg.refresh_freq)

                elif data['code'] == -1000:
                    self.bot.send_message(cg.errors, 'Token expired')
                    self.bot.send_message(cg.admin, 'Token expired')
                    print(f'{now_is()} - Token expired\n')
                    break

                else:
                    self.bot.send_message(cg.errors, f'Unhandled response : {data}')
                    print(f'{now_is()} - Unhandled response while checking lives: {data}\n')
                    break
            except Exception as e:
                self.bot.send_message(cg.errors, f'Error while checking lives : {e}')
                print(f'{now_is()} - Error while checking lives : {e}\n')
