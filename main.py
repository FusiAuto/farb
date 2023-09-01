import os
import pyrostep
import DATA.common_globals as cg
from pyrogram import Client, filters, idle
from FUSI.Monitor import Monitor
from COM.now_is import now_is
from TG_BOT.keyboards import keyboards

PATH = os.getcwd()

if not os.path.isdir(f'{PATH}/VIDS/TEMP'):
    os.makedirs(f'{PATH}/VIDS/TEMP')

bot = Client("fusi-render",
             api_id=os.environ['API_ID'],
             api_hash=os.environ['API_HASH'],
             bot_token=os.environ['BOT_TOKEN'])

pyrostep.listen(bot)


@bot.on_message(filters.command('start'))
async def start_command(client, msg):
    await msg.reply('Alive')


@bot.on_message(filters.command('menu'))
async def menu_command(client, msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    await bot.delete_messages(cid, msg.id)
    await bot.send_message(cid, 'MAIN MENU'
                                '\n\nSelect option',
                           reply_markup=keyboards('menu', uid))


@bot.on_message(filters.command('freq'))
async def freq_command(client, msg):
    uid = msg.from_user.id
    await msg.reply(f'Set monitor refresh frequency in seconds'
                    f'\n\nCurrent frequency : {cg.refresh_freq}s',
                    reply_markup=keyboards('freq_main', uid))


@bot.on_callback_query()
async def callback_query(client, call):
    cid = call.message.chat.id
    mid = call.message.id

    # CLOSE
    if call.data.startswith('close'):
        uid = call.data.split('.')[1]
        await pyrostep.unregister_steps(uid)
        await bot.delete_messages(cid, mid)

    # MENU
    if call.data == 'menu':
        await bot.edit_message_text(cid, mid, 'MAIN MENU'
                                              '\n\nSelect option',
                                    reply_markup=keyboards('menu'))

    # FREQUENCY
    if call.data.startswith('freq_main'):
        uid = call.data.split('.')[1]
        if uid is not None:
            await pyrostep.unregister_steps(uid)
        await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                              f'\n\nCurrent frequency : {cg.refresh_freq}s',
                                    reply_markup=keyboards('freq_main', uid))

    if call.data.startswith('freq_set'):
        uid = call.data.split('.')[1]
        print(call.data)
        print(uid)
        await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                              f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                              f'\n\nEnter value in seconds (min 1 - 60 max)',
                                    reply_markup=keyboards('freq_back', uid))
        await pyrostep.register_next_step(uid, freq_set)


# STEP HANDLERS
async def freq_set(client, msg):
    print(msg.text)


try:
    bot.stop()
except ConnectionError:
    pass

bot.start()
monitor = Monitor(bot, PATH)
monitor.start()
print(f'{now_is()} - {cg.GREEN}BOT STARTED{cg.RESET}\n')
idle()
bot.stop()
