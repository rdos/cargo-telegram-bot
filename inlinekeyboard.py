#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic example for a bot that uses inline keyboards.
# https://api.telegram.org/bot478909799:AAEuh8FPg_kEcbAJmB5O8En8Rmbzly2rT_I/getUpdates
# This program is dedicated to the public domain under the CC0 license.
"""

import logging
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    levePl=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2'),
                 InlineKeyboardButton("Option 3", callback_data='3'),
                 InlineKeyboardButton("Option 3", callback_data='3'),
                 InlineKeyboardButton("Option 3", callback_data='3')],
                [InlineKeyboardButton("Option 4", callback_data='4')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(bot, update):
    print(type(update.callback_query).__name__)
    query_d = update.callback_query.to_dict()
    print(query_d)
    # print("")
    print(query_d['from']['first_name'])
    # print("")
    # print(query_d['message'])
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=chat_id,
                          message_id=query.message.message_id)

    conn = sqlite3.connect('C:/tt/cargo.sqlite')
    sql_text = ''' INSERT INTO notice_t(user_name,user_id,chat_id,message_id)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    project = (query_d['from']['first_name'], query_d['from']['id'], chat_id, message_id)
    cur.execute(sql_text, project)
    conn.commit()
    conn.close()

def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("478909799:AAEuh8FPg_kEcbAJmB5O8En8Rmbzly2rT_I")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('ttest', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()




if __name__ == '__main__':
    main()
