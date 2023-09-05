import os
from threading import Thread, Lock
from FUSI.GetLink import GetLink
from FUSI.Record import Record
import DATA.common_globals as cg
from COM.get_video_data import get_video_data
from FUSI.m3u8_connection import m3u8_test
from COM.thumbnails import gen_thumbs
from pyrogram.errors import RPCError


class AutoRecHandler(Thread):
    def __init__(self, bot, path, uid, live_data) -> None:
        Thread.__init__(self)
        self.bot = bot
        self.path = path
        self.uid = uid
        self.live_data = live_data
        self.lock = Lock()

    def run(self):
        link = GetLink(self.bot, self.uid)
        link.get_link()
        if link.hls is not None:
            if m3u8_test(self.bot, link.hls):
                rec = Record(self.bot, self.path, link.hls, self.live_data, link.country)
                rec.start()
                rec.join()
                with self.lock:
                    try:
                        cg.current_records.remove(self.uid)
                    except KeyError:
                        pass

                status = rec.status
                if status:
                    filename = rec.filename
                    data = get_video_data(filename)
                    tg_filename = filename[filename.rfind('/') + 1:]
                    uid = self.live_data['uid']
                    name = self.live_data['name']
                    title = self.live_data['title']
                    caption = tg_filename.split('.')[0].split('-')
                    caption = (f'{caption[1]}-{caption[2]}-{caption[3]} '
                               f'{caption[4]}:{caption[5]}:{caption[6]}'
                               f'\n\nFUSI ID : {uid}'
                               f'\nNAME : {name}'
                               f'\nTITLE : {title}')

                    if data['size'] < 10485760:  # 10 MB MINIMUM TO SET THUMBNAILS ON TELEGRAM
                        bm = self.bot.send_video(cg.target, filename,
                                                 caption=caption,
                                                 duration=data['duration'],
                                                 width=data['width'],
                                                 height=data['height'],
                                                 file_name=tg_filename,
                                                 supports_streaming=True)

                    else:
                        thumbs = gen_thumbs(filename, data)
                        if thumbs is not None:
                            bm = self.bot.send_video(cg.target, filename,
                                                     caption=caption,
                                                     duration=data['duration'],
                                                     width=data['width'],
                                                     height=data['height'],
                                                     thumb=thumbs,
                                                     file_name=tg_filename,
                                                     supports_streaming=True)
                            if bm is not None:
                                os.remove(thumbs)

                        else:
                            bm = self.bot.send_video(cg.target, filename,
                                                     caption=caption,
                                                     duration=data['duration'],
                                                     width=data['width'],
                                                     height=data['height'],
                                                     file_name=tg_filename,
                                                     supports_streaming=True)
                    if bm is not None:
                        os.remove(filename)
                        video = bm.video.file_id
                        for user in cg.notify_users:
                            try:
                                self.bot.send_video(user, video,
                                                    caption=caption)
                            except RPCError:
                                pass
