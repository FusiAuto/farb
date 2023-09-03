RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

user_token = '6c12e6567060403295a4509881cefb55'     # in config file / change with bot command
user_uid = 5687609                                  # in config file / change with bot command
admin = 1794541520                                  # os.environ(['ADMIN'])
target = 1794541520                                 # first None / in config file / change with bot command
errors = 0                                          # first None / in config file / change with bot command
notify_users = set()
notify_users.add(admin)

current_records = set()

refresh_freq = 1                                    # default 1 / in config file / change with bot command
