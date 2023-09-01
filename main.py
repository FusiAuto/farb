import os
import DATA.common_globals as cg
from FUSI.Monitor import Monitor
from pyrogram import Client, filters, idle
from COM.now_is import now_is


bot = Client("fusi-render",
             api_id=os.environ['API_ID'],
             api_hash=os.environ['API_HASH'],
             bot_token=os.environ['BOT_TOKEN'])


@bot.on_message(filters.command('start'))
async def start_command(client, msg):
    cid = msg.chat.id


bot.start()
monitor = Monitor(bot)
monitor.start()
print(f'{now_is()} - {cg.GREEN}BOT STARTED{cg.RESET}\n')
idle()
bot.stop()
