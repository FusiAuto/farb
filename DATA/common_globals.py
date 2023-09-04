RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
YELLOW = '\u001b[33m'
RESET = '\033[0m'

lives_url = "https://cpapi.footseen.xyz/room/queryUserLikeList"
links_url = "https://cpapi.footseen.xyz/room/enterRoom"
host = "cpapi.footseen.xyz"
page_id = "56f901109e787c055c5ca8bd872fe88b"
referer = "https://www.footseen.xyz/"

user_token = '6c12e6567060403295a4509881cefb55'     # in config file / change with bot command
user_uid = 5687609                                  # in config file / change with bot command
admin = 1794541520                                  # os.environ(['ADMIN'])
target = -1001869200508                             # first None / in config file / change with bot command
errors = -1001854111266                             # first None / in config file / change with bot command
notify_users = set()
notify_users.add(admin)

current_records = set()

refresh_freq = 1                                    # default 1 / in config file / change with bot command
