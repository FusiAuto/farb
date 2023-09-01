import requests
import DATA.common_globals as cg


class GetLink:
    def __init__(self, bot, uid):
        self.bot = bot
        self.uid = uid
        self.url = "https://cpapi.footseen.xyz/room/enterRoom"
        self.querystring = {
            "lang": "1",
            "os": "h5",
            "cid": "ftsH5",
            "webVersion": "1000",
            "roomId": uid,
            "pageID": "56f901109e787c055c5ca8bd872fe88b"
        }
        self.headers = {
            "Host": "cpapi.footseen.xyz",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "user-agent": "Mozilla/5.0 (Linux; Android 7.1.2; ASUS_Z01QD) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36",
            "origin": "origin",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.footseen.xyz/",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9"
        }
        self.hls = None
        self.country = None

    def get_link(self):
        try:
            with requests.get(self.url, params=self.querystring, headers=self.headers) as response:
                if response.status_code == 200:
                    r = response.json()
                    if r['msg'] == 'successful':
                        self.hls = r['pullFlowUrlHLS']
                        self.country = r['roomBaseInfo']['addr']

                else:
                    print(f'Error while taking link : {response.status_code}')
                    # self.bot.send_message(cg.admin, f'Error while taking link : {response.status_code}')

        except requests.exceptions.SSLError:
            # self.bot.send_message(cg.admin, 'Connection error, try again in few seconds')
            print('Connection error, try again in few seconds')
            cg.current_records.remove(self.uid)

        except requests.exceptions.ConnectionError:
            # self.bot.send_message(cg.admin, 'Connection error, try again in few seconds')
            print('Connection error, try again in few seconds')
            cg.current_records.remove(self.uid)

        except Exception as e:
            # self.bot.send_message(cg.admin, f'Exception : {e}')
            print(f'Exception : {e}')
            cg.current_records.remove(self.uid)
