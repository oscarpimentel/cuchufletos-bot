import os
import pprint
import json
from datetime import datetime

import cambriantools as ct
from dynaconf import settings

from . import utils


class Cuchubot():
    def __init__(self):
        self.reset()

    def reset(self):
        self.good_counter = 0
        self.bad_counter = 0
        self.actual_name = None
        self.mvp = None

    @classmethod
    def get_methods(cls):
        cuchubot = cls()
        return [method for method in dir(cuchubot) if method[:3] == 'tf_']

    def get_name(self,
                 uses_extra_info=False,
                 ):
        final_name, names_used, last_names_used = utils.generate_cuchufletos_names()
        extra_info = ' (' + '+'.join([
            f'{name_used} {last_name_used}'
            for name_used, last_name_used in zip(names_used, last_names_used)
        ]) + ')'
        txt = f'{final_name}{extra_info if uses_extra_info else ""}'
        self.actual_name = final_name
        return txt

    def __repr__(self,
                 compact=True,
                 pprint_objs=[dict, list, tuple],
                 ):
        txt = f'{self.__class__.__name__}' + ('(' if compact else '(\n')
        txts = []
        for k, v in self.__dict__.items():
            if k.startswith('__'):
                continue
            elif type(v) in pprint_objs:
                vstr = pprint.pformat(v)
            elif type(v) == str:
                vstr = f"'{v}'"
            else:
                vstr = str(v)
            vstr = vstr[:-1] if vstr[-1] == '\n' else vstr
            txts += [f'{k}={vstr}']
        txt += ('; ' if compact else ';\n').join(txts)
        txt += ')' if compact else '\n)'
        return txt

    def tf_caracola(self, update, context,
                    debug=False,
                    ):
        txt, lang_tld = utils.read_caracola()
        audio_filedir = utils.generate_audio_file(txt, lang_tld)
        open(audio_filedir, 'rb')
        in_txt = '' if debug else update.message.text.replace('/caracola', '')
        out_txt = f'Consulta: {in_txt}\nLa caracola cuchufleta dice:'
        txt, lang_tld = utils.read_caracola()
        audio_filedir = utils.generate_audio_file(txt, lang_tld)
        if debug:
            return txt, audio_filedir
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=out_txt)
            context.bot.send_audio(
                chat_id=update.effective_chat.id, audio=open(audio_filedir, 'rb'))

    def tf_grade(self, update, context,
                 debug=False,
                 ):
        filedir = os.path.join(settings.DATA_PATH, settings.PERSONS_FILENAME)
        persons = json.load(open(filedir))['cuchus']
        out_txt = ''
        out_txt += 'Titulado?\n'
        for person in persons:
            full_name = person.pop('full_name')
            graded = 'si' if person['graded'] else 'no'
            out_txt += f'\t{full_name} {graded}\n'
        if debug:
            return out_txt
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=out_txt)

    def tf_curse(self, update, context,
                 debug=False,
                 ):
        filedir = os.path.join(settings.DATA_PATH, settings.PERSONS_FILENAME)
        persons = json.load(open(filedir))['cursed_persons']
        person = ct.lists.get_random_item(persons)
        full_name = person.pop('full_name')
        img_url = person.pop('img_url')
        out_txt = ''
        out_txt += f'{full_name}\n'
        out_txt += '\n'.join([person[k] for k in person.keys()])
        if debug:
            return out_txt
        else:
            context.bot.send_photo(
                chat_id=update.effective_chat.id, photo=img_url)
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=out_txt)

    def tf_name(self, update, context,
                debug=False,
                ):
        out_txt = self.get_name()
        if debug:
            return out_txt
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=out_txt)

    def tf_fullname(self, update, context,
                    debug=False,
                    ):
        out_txt = self.get_name(uses_extra_info=True)
        if debug:
            return out_txt
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=out_txt)

    def tf_iswed(self, update, context, debug=False):
        now = datetime.now()
        if datetime.weekday(now) == 2:
            img_name = 'normal' if now.month != 12 else 'christmas'
            if debug:
                return f'It is {img_name} Wednesday, my dudes'
            img_url = os.path.join(settings.DATA_PATH, 
                                   f'./images/iswed/{img_name}.jpg')
            context.bot.send_photo(chat_id=update.effective_chat.id,
                                   photo=open(img_url, 'rb'))
        else:
            out_txt = 'It is not Wednesday, my dudes :('
            if debug:
                return out_txt
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=out_txt)
