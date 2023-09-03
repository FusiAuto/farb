import os
import time
import requests
from flask import Flask
from threading import Thread
import logging


app = Flask('')
logging.getLogger('werkzeug').disabled = True


@app.route('/')
def main():
    # monitor = False
    # for thread in threading.enumerate():
    #     if thread.name == 'MONITOR':
    #         monitor = True
    #
    # if not monitor:
    #     pass

    return "BOT is alive!"


def run():
    app.run(host="0.0.0.0", port=8080)


def ping():
    url = 'http://127.0.0.1:8080/'
    # url = os.environ['SELF_URL']
    while True:
        requests.request("GET", url)
        time.sleep(1)


def keep_alive():
    server = Thread(target=run)
    server.name = 'SERVER'
    server.start()
    monitor = Thread(target=ping)
    monitor.name = 'PING'
    monitor.start()
