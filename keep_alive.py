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
    return "Your bot is alive!"


def run():
    app.run(host="0.0.0.0", port=8080)


def ping():
    url = os.environ['SELF_URL']
    while True:
        requests.request("GET", url)
        time.sleep(1)


def keep_alive():
    server = Thread(target=run)
    server.start()
    monitor = Thread(target=ping)
    monitor.start()
