import os

from dynaconf import settings

from cuchubot.bots import Cuchubot


def get_token(filedir=None):
    filedir = os.path.join(settings.DATA_PATH, 'token') if filedir is None else filedir
    with open(filedir) as f:
        return f.readlines()[0].replace('\n', '')


def help(update, context):
    """
    Send a message when the command /help is issued.
    """
    txt = 'methods:\n'
    txt += '\n'.join([f"/{method.replace('tf_', '')}" for method in Cuchubot.get_methods()])
    update.message.reply_text(txt)