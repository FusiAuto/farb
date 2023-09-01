import ffmpeg
from threading import Thread
from datetime import datetime
import DATA.common_globals as cg
from COM.now_is import now_is


class Record(Thread):
    def __init__(self, bot, path, url, live_data, country=None):

        Thread.__init__(self)
        self.bot = bot
        self.url = url
        self.uid = live_data['uid']
        self.u_name = live_data['name']
        self.title = live_data['title']
        self.country = country
        now = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        self.filename = f'{path}/VIDS/{self.uid}-{now}.mp4'
        self.status = False

    def run(self):

        print(f'\n{now_is()} - {cg.GREEN}AUTO Recording{cg.RESET} {cg.BLUE}ID {self.uid}  |  {self.u_name}'
              f'\n                                     COUNTRY : {self.country}'
              f'\n                                     TITLE : {self.title}{cg.RESET}\n')
        self.bot.send_message(cg.admin, f'⏺ 🎥 AUTO Recording [ID {self.uid}  |  {self.u_name}]({self.url})'
                                        f'\nCOUNTRY : {self.country}'
                                        f'\nTITLE : {self.title}')
        try:
            stream = ffmpeg.input(self.url)
            stream = ffmpeg.output(stream, self.filename, codec='copy')
            stream = stream.global_args('-nostdin')
            rec = ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            err = rec[1].decode('utf-8')
        except ffmpeg.Error as e:
            err = e.stderr.decode('utf-8')

            print(f'\n{now_is()} - {cg.RED}ffmpeg error{cg.RESET} : {err}\n')
            self.bot.send_message(cg.admin, f'ffmpeg error : {err}')

        if 'time=' in err:
            time = err[err.rfind('time=') + 5:].split('.')[0]

            print(f'\n{now_is()} - {cg.GREEN}Record finished{cg.RESET} '
                  f'{cg.BLUE}ID {self.uid}  |  {self.u_name} - {time}{cg.RESET}\n')
            self.bot.send_message(cg.admin, f'⏹ 📼 Record finished ID {self.uid}  |  {self.u_name}  - {time}')

            self.status = True
