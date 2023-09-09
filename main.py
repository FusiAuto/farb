import os
import threading
import pyrostep
import DATA.common_globals as cg
from pyrogram import Client, filters, idle
from FUSI.Monitor import Monitor
from COM.now_is import now_is
from TG_BOT.keyboards import keyboards
from keep_alive import keep_alive

PATH = os.getcwd()

if not os.path.isdir(f'{PATH}/VIDS/TEMP'):
    os.makedirs(f'{PATH}/VIDS/TEMP')

bot = Client("fusi-render",
             api_id=os.environ['API_ID'],
             api_hash=os.environ['API_HASH'],
             bot_token=os.environ['BOT_TOKEN'],
             max_concurrent_transmissions=4)

pyrostep.listen(bot)

user_menu = {}


@bot.on_message(filters.command('start'))
async def start_command(client, msg):
    await msg.reply('Alive')


@bot.on_message(filters.command('current'))
async def c_command(client, msg):
    await msg.reply(cg.current_records)


@bot.on_message(filters.command('unlock'))
async def u_command(client, msg):
    await msg.reply('Tap ID to unlock', reply_markup=keyboards('unlock'))


@bot.on_message(filters.command('threads'))
async def t_command(client, msg):
    text = ''
    for thread in threading.enumerate():
        text = text + str(thread).lstrip('<').rstrip('>') + '\n\n'
    await msg.reply(text)


@bot.on_message(filters.command('menu'))
async def menu_command(client, msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    await bot.delete_messages(cid, msg.id)
    bm = await bot.send_message(cid, 'MAIN MENU'
                                     '\n\nSelect option',
                                reply_markup=keyboards('menu', uid))
    user_menu[uid] = bm


@bot.on_callback_query()
async def callback_query(client, call):
    cid = call.message.chat.id
    mid = call.message.id
    try:
        uid = int(call.data.split('.')[1])
    except IndexError:
        uid = 0

    # CLOSE
    if call.data.startswith('close'):
        await pyrostep.unregister_steps(uid)
        await bot.delete_messages(cid, mid)
        del user_menu[uid]

    # MENU
    if call.data.startswith('menu'):
        await bot.edit_message_text(cid, mid, 'MAIN MENU'
                                              '\n\nSelect option',
                                    reply_markup=keyboards('menu', uid))

    # FREQUENCY
    if call.data.startswith('freq_main'):
        if uid is not None:
            await pyrostep.unregister_steps(uid)
        await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                              f'\n\nCurrent frequency : {cg.refresh_freq}s',
                                    reply_markup=keyboards('freq_main', uid))

    if call.data.startswith('freq_set'):
        await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                              f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                              f'\n\nEnter value in seconds (min 1 - 60 max)',
                                    reply_markup=keyboards('freq_back', uid))
        await pyrostep.register_next_step(uid, freq_set)

    # UNLOCK
    if call.data.startswith('unlock'):
        unlock_id = int(call.data.split('.')[1])
        try:
            cg.current_records.remove(unlock_id)
            await bot.edit_message_text(cid, mid, 'Tap ID to unlock', reply_markup=keyboards('unlock'))
        except KeyError:
            pass

    if call.data == 'exit':
        await bot.delete_messages(cid, mid)


# STEP HANDLERS
async def freq_set(client, msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    mid = user_menu[uid].id
    await bot.delete_messages(cid, msg.id)

    if msg.text is None:
        await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                              f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                              f'\n\nEnter value in seconds (min 1 - 60 max)'
                                              f'\n\n!!! Value must be digit !!!',
                                    reply_markup=keyboards('freq_back', uid))
        await pyrostep.register_next_step(uid, freq_set)

    else:
        if msg.text.isdigit():
            new = int(msg.text)
            if new < 1:
                await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                                      f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                                      f'\n\nEnter value in seconds (min 1 - 60 max)'
                                                      f'\n\n!!! Value to low  !!!',
                                            reply_markup=keyboards('freq_back', uid))
                await pyrostep.register_next_step(uid, freq_set)

            elif new > 60:
                await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                                      f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                                      f'\n\nEnter value in seconds (min 1 - 60 max)'
                                                      f'\n\n!!! Value to high  !!!',
                                            reply_markup=keyboards('freq_back', uid))
                await pyrostep.register_next_step(uid, freq_set)

            elif new == cg.refresh_freq:
                await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                                      f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                                      f'\n\nSame value nothing changed',
                                            reply_markup=keyboards('freq_main', uid))

            else:
                cg.refresh_freq = new
                # save
                await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                                      f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                                      f'\n\nFrequency changed',
                                            reply_markup=keyboards('freq_main', uid))

        else:
            await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                                  f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                                  f'\n\nEnter value in seconds (min 1 - 60 max)'
                                                  f'\n\n!!! Value must be digit !!!',
                                        reply_markup=keyboards('freq_back', uid))
            await pyrostep.register_next_step(uid, freq_set)


try:
    bot.stop()
except ConnectionError:
    pass

bot.start()

monitor = Monitor(bot, PATH)
monitor.start()
# keep_alive()
#
print(f'{now_is()} - {cg.GREEN}BOT STARTED{cg.RESET}\n')
idle()
bot.stop()
