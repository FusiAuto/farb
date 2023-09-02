from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboards(keyboard, param=None):

    if keyboard == 'menu':
        btn1 = InlineKeyboardButton('MONITOR FREQUENCY', callback_data=f'freq_main.{param}')
        btn2 = InlineKeyboardButton('empty', callback_data='xxx')
        btn3 = InlineKeyboardButton('CLOSE', callback_data=f'close.{param}')
        buttons = [btn1, btn2, btn3]
        kb = InlineKeyboardMarkup([buttons])
        return kb

    if keyboard == 'freq_main':
        btn1 = InlineKeyboardButton('CHANGE', callback_data=f'freq_set.{param}')
        btn2 = InlineKeyboardButton('BACK', callback_data=f'menu.{param}')
        btn3 = InlineKeyboardButton('CLOSE', callback_data=f'close.{param}')
        buttons = [btn1, btn2, btn3]
        kb = InlineKeyboardMarkup([buttons])
        return kb

    if keyboard == 'freq_back':
        btn1 = InlineKeyboardButton('BACK', callback_data=f'freq_main.{param}')
        btn2 = InlineKeyboardButton('CLOSE', callback_data=f'close.{param}')
        buttons = [btn1, btn2]
        kb = InlineKeyboardMarkup([buttons])
        return kb
