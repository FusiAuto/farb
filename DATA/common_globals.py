import os

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
YELLOW = '\u001b[33m'
RESET = '\033[0m'

PATH = None

# HIDDEN API

# # server version - env
# lives_url = os.environ['lives_url']
# links_url = os.environ['links_url']
# host = os.environ['host']
# page_id = os.environ['page_id']
# referer = os.environ['referer']

# local version - file
lives_url = None
links_url = None
host = None
page_id = None
referer = None


# COMMON FROM CONFIG FILE
fs_user_token = None
fs_user_uid = None
MASTER = None
target = None
errors = None
refresh_freq = 1
admins = set()
notify_users = set()

current_records = set()

