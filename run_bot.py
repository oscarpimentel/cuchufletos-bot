#!/usr/bin/env python3
# -*- coding: utf-8 -*
import argparse

import logging
from telegram.ext import Updater, CommandHandler
from cuchubot.bots import Cuchubot

import utils


def error(update, context):
    """
    Log Errors caused by Updates.
    """
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# parser
parser = argparse.ArgumentParser(prefix_chars='--')
parser.add_argument('--debug', action='store_true')
main_args = parser.parse_args()


# define bot
cuchubot = Cuchubot()
if main_args.debug:
    for method in Cuchubot.get_methods():
        repeats = 10 if method in ['tf_caracola'] else 1
        for _ in range(0, repeats):
            print(f'{method}:')
            print(getattr(cuchubot, method)(None, None, debug=True))
    raise SystemExit


# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
token = utils.get_token()
updater = Updater(token, use_context=True)
dp = updater.dispatcher  # Get the dispatcher to register handlers
# on different commands - answer in Telegram
dp.add_handler(CommandHandler('help', help))
for method in Cuchubot.get_methods():
    new_method = method.replace('tf_', '')
    dp.add_handler(CommandHandler(new_method, getattr(cuchubot, method)))
dp.add_error_handler(error)  # log all errors
# Start the Bot
updater.start_polling()
updater.idle()
