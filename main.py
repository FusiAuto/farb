import os
import threading
import pyrostep
import DATA.common_globals as cg
from pyrogram import Client, filters, idle, enums
from pyrogram.errors import RPCError
from COM.config import config
from COM.save import save
from FUSI.Monitor import Monitor
from COM.now_is import now_is
from TG_BOT.keyboards import keyboards
# from keep_alive import keep_alive


cg.PATH = os.getcwd()


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
    if len(cg.current_records) > 0:
        await msg.reply(cg.current_records)
    else:
        await msg.reply('Empty')


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
                                              f'\n\nEnter value in seconds (min 1 - 60 max) 💬',
                                    reply_markup=keyboards('freq_back', uid))
        await pyrostep.register_next_step(uid, freq_set)

    # VIDEO TARGET
    if call.data.startswith('target_main'):
        await pyrostep.unregister_steps(uid)
        if cg.target is None:
            await bot.edit_message_text(cid, mid, f'Set basic target group for videos',
                                        reply_markup=keyboards('target_main', uid))
        else:
            await bot.edit_message_text(cid, mid, f'Change basic target group for videos'
                                                  f'\n\nCurrent target ID : {cg.target}',
                                        reply_markup=keyboards('target_main', uid))

    if call.data.startswith('target_set'):
        if cg.target is None:
            await bot.edit_message_text(cid, mid, f'Set basic target group for videos'
                                                  f'\n\nEnter group ID 💬',
                                        reply_markup=keyboards('target_back', uid))
        else:
            await bot.edit_message_text(cid, mid, f'Change basic target group for videos'
                                                  f'\n\nCurrent target ID : {cg.target}'
                                                  f'\n\nEnter group ID 💬',
                                        reply_markup=keyboards('target_back', uid))
        await pyrostep.register_next_step(uid, target_set)

    # ERROR TARGET
    if call.data.startswith('error_main'):
        await pyrostep.unregister_steps(uid)
        if cg.target is None:
            await bot.edit_message_text(cid, mid, f'Set basic target group for errors',
                                        reply_markup=keyboards('error_main', uid))
        else:
            await bot.edit_message_text(cid, mid, f'Change basic target group for errors'
                                                  f'\n\nCurrent errors log ID : {cg.errors}',
                                        reply_markup=keyboards('error_main', uid))

    if call.data.startswith('error_set'):
        if cg.target is None:
            await bot.edit_message_text(cid, mid, f'Set basic target group for errors'
                                                  f'\n\nEnter errors log group ID 💬',
                                        reply_markup=keyboards('error_back', uid))
        else:
            await bot.edit_message_text(cid, mid, f'Change basic target group for errors'
                                                  f'\n\nCurrent errors log ID : {cg.errors}'
                                                  f'\n\nEnter errors log group ID 💬',
                                        reply_markup=keyboards('error_back', uid))
        await pyrostep.register_next_step(uid, error_set)

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
        try:
            await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                                  f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                                  f'\n\nEnter value in seconds (min 1 - 60 max) 💬'
                                                  f'\n\n❌ Value must be digit ‼️',
                                        reply_markup=keyboards('freq_back', uid))
        except RPCError:
            pass
        await pyrostep.register_next_step(uid, freq_set)

    else:
        if msg.text.isdigit():
            new = int(msg.text)
            if new < 1:
                try:
                    await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                                          f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                                          f'\n\nEnter value in seconds (min 1 - 60 max) 💬'
                                                          f'\n\n❌ Value to low ‼️',
                                                reply_markup=keyboards('freq_back', uid))
                except RPCError:
                    pass
                await pyrostep.register_next_step(uid, freq_set)

            elif new > 60:
                try:
                    await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                                          f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                                          f'\n\nEnter value in seconds (min 1 - 60 max) 💬'
                                                          f'\n\n❌ Value to high ‼️',
                                                reply_markup=keyboards('freq_back', uid))
                except RPCError:
                    pass
                await pyrostep.register_next_step(uid, freq_set)

            elif new == cg.refresh_freq:
                await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                                      f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                                      f'\n\n☑️ Same value nothing changed',
                                            reply_markup=keyboards('freq_main', uid))

            else:
                cg.refresh_freq = new
                save(cg.refresh_freq, f'{cg.PATH}/DATA/refresh_freq')
                await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                                      f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                                      f'\n\n✅ Frequency changed',
                                            reply_markup=keyboards('freq_main', uid))

        else:
            try:
                await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                                      f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                                      f'\n\nEnter value in seconds (min 1 - 60 max) 💬'
                                                      f'\n\n❌ Value must be digit ‼️',
                                            reply_markup=keyboards('freq_back', uid))
            except RPCError:
                pass
            await pyrostep.register_next_step(uid, freq_set)


async def target_set(client, msg):

    cid = msg.chat.id
    uid = msg.from_user.id
    mid = user_menu[uid].id
    await bot.delete_messages(cid, msg.id)

    if msg.text is None:
        try:
            await bot.edit_message_text(cid, mid, f'Change basic target group for videos'
                                                  f'\n\nCurrent target ID : {cg.target}'
                                                  f'\n\n❌ Value must be negative digit ‼️'
                                                  f'\n\nEnter group ID 💬',
                                        reply_markup=keyboards('target_back', uid))
        except RPCError as e:
            pass
        await pyrostep.register_next_step(uid, target_set)

    else:
        try:
            target = int(msg.text)
            if target > 0:
                try:
                    await bot.edit_message_text(cid, mid, f'Change basic target group for videos'
                                                          f'\n\nCurrent target ID : {cg.target}'
                                                          f'\n\n❌ Value must be negative digit ‼️'
                                                          f'\n\nEnter group ID 💬',
                                                reply_markup=keyboards('target_back', uid))
                except RPCError:
                    pass
                await pyrostep.register_next_step(uid, target_set)

            else:
                try:
                    await bot.send_chat_action(target, enums.ChatAction.TYPING)
                    cg.target = target
                    save(cg.target, f'{cg.PATH}/DATA/target')
                    await bot.edit_message_text(cid, mid, f'Change basic target group for videos'
                                                          f'\n\nCurrent target ID : {cg.target}'
                                                          f'\n\n✅ Target changed',
                                                reply_markup=keyboards('target_main', uid))
                except RPCError as e:
                    try:
                        await bot.edit_message_text(cid, mid, f'Change basic target group for videos'
                                                              f'\n\nCurrent target ID : {cg.target}'
                                                              f'\n\n⛔️ BOT can\'t write in this group'
                                                              f'\n\nEnter group ID 💬',
                                                    reply_markup=keyboards('target_back', uid))
                    except RPCError:
                        pass
                    await pyrostep.register_next_step(uid, target_set)

        except ValueError:
            try:
                await bot.edit_message_text(cid, mid, f'Change basic target group for videos'
                                                      f'\n\nCurrent target ID : {cg.target}'
                                                      f'\n\n❌ Value must be negative digit ‼️'
                                                      f'\n\nEnter group ID 💬',
                                            reply_markup=keyboards('target_back', uid))
            except RPCError:
                pass
            await pyrostep.register_next_step(uid, target_set)


async def error_set(client, msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    mid = user_menu[uid].id
    await bot.delete_messages(cid, msg.id)

    if msg.text is None:
        try:
            await bot.edit_message_text(cid, mid, f'Change basic target group for errors'
                                                  f'\n\nCurrent errors log ID : {cg.target}'
                                                  f'\n\n❌ Value must be negative digit ‼️'
                                                  f'\n\nEnter errors log group ID 💬',
                                        reply_markup=keyboards('error_back', uid))
        except RPCError as e:
            pass
        await pyrostep.register_next_step(uid, error_set)

    else:
        try:
            errors = int(msg.text)
            if errors > 0:
                try:
                    await bot.edit_message_text(cid, mid, f'Change basic target group for errors'
                                                          f'\n\nCurrent errors log ID : {cg.errors}'
                                                          f'\n\n❌ Value must be negative digit ‼️'
                                                          f'\n\nEnter errors log group ID 💬',
                                                reply_markup=keyboards('error_back', uid))
                except RPCError:
                    pass
                await pyrostep.register_next_step(uid, error_set)

            else:
                try:
                    await bot.send_chat_action(errors, enums.ChatAction.TYPING)
                    cg.errors = errors
                    save(cg.errors, f'{cg.PATH}/DATA/errors')
                    await bot.edit_message_text(cid, mid, f'Change basic target group for errors'
                                                          f'\n\nCurrent errors log ID : {cg.errors}'
                                                          f'\n\n✅ Errors log group changed',
                                                reply_markup=keyboards('error_main', uid))
                except RPCError as e:
                    try:
                        await bot.edit_message_text(cid, mid, f'Change basic target group for errors'
                                                              f'\n\nCurrent errors log ID : {cg.errors}'
                                                              f'\n\n⛔️ BOT can\'t write in this group'
                                                              f'\n\nEnter errors log group ID 💬',
                                                    reply_markup=keyboards('error_back', uid))
                    except RPCError:
                        pass
                    await pyrostep.register_next_step(uid, error_set)

        except ValueError:
            try:
                await bot.edit_message_text(cid, mid, f'Change basic target group for errors'
                                                      f'\n\nCurrent errors log ID : {cg.errors}'
                                                      f'\n\n❌ Value must be negative digit ‼️'
                                                      f'\n\nEnter errors log group ID 💬',
                                            reply_markup=keyboards('error_back', uid))
            except RPCError:
                pass
            await pyrostep.register_next_step(uid, error_set)

try:
    bot.stop()
except ConnectionError:
    pass

bot.start()

config()
monitor = Monitor(bot)
monitor.start()
# keep_alive()

print(f'{now_is()} - {cg.GREEN}BOT STARTED{cg.RESET}\n')
idle()
bot.stop()
