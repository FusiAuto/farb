import os

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
YELLOW = '\u001b[33m'
RESET = '\033[0m'

# # server version
# lives_url = os.environ['lives_url']
# links_url = os.environ['links_url']
# host = os.environ['host']
# page_id = os.environ['page_id']
# referer = os.environ['referer']

# local version
lives_url = None
links_url = None
host = None
page_id = None
referer = None


fs_user_token = '6c12e6567060403295a4509881cefb55'     # in config file / change with bot command
fs_user_uid = 5687609                                  # in config file / change with bot command
MASTER = 1794541520                                  # os.environ['ADMIN'] / config file
target = -1001869200508                             # first None / in config file / change with bot command
errors = -1001854111266                             # first None / in config file / change with bot command
admins = []
notify_users = set()
notify_users.add(MASTER)

current_records = set()

refresh_freq = 1                                    # default 1 / in config file / change with bot command
