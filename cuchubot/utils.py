import os
import itertools
import re

import toml
import numpy as np
import pandas as pd
import cambriantools as ct
from gtts import gTTS
from dynaconf import settings


VOCALS = 'aeiou'
CONSTANTS = 'qwrtypsdfghjklñzxcvbnm'
CORRECT_VOCALS = ['ei', 'ae', 'io']
CORRECT_CONSONANTS = ['pp']
CONSONANTIC_GROUP = ['bl', 'br', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr', 'pl', 'pr', 'tl', 'tr'] + CORRECT_VOCALS + CORRECT_CONSONANTS


def format_inner_lists(txt):
    if txt.find('[') == -1:
        return txt
    txt = txt.replace('[', '(').replace(']', ')')
    while True:
        re_search = re.search('\(([^)]+)', txt)
        if re_search is None:
            break
        in_txt = re_search.group(1)
        in_txt = np.random.choice(in_txt.split(','))
        txt = txt[0:re_search.start()] + in_txt + txt[re_search.end() + 1:]
    return txt


def read_caracola(returns_original_txt=False):
    filedir = os.path.join(settings.DATA_PATH, settings.CARACOLA_FILENAME)
    df = pd.read_excel(filedir, sheet_name='data')
    df = df.dropna(how='all')
    row_df = df.sample(weights='repeats')
    original_txt = row_df['text'].values[0]
    lang_tld = row_df['lang'].values[0]
    txt = format_inner_lists(original_txt)
    if returns_original_txt:
        return txt, lang_tld, original_txt
    else:
        return txt, lang_tld


def generate_audio_file(txt, lang_tld):
    lang_tld = 'es-com.mx' if lang_tld is None else lang_tld
    lang, tld = lang_tld.split('-')
    tts = gTTS(txt, lang=lang, tld=tld)
    filedir = os.path.join(settings.TEMP_PATH, settings.CARACOLA_AUDIO_FILENAME)
    tts.save(filedir)
    return filedir


def get_combinations(elements):
    combinations = list(itertools.product(elements, repeat=2))
    return [pair[0] + pair[1] for pair in combinations]


def acceptable_name(name, wrong_elements,
                    min_length=4,
                    ):
    if len(name) < min_length:
        return False
    for i in range(len(name)):
        sub = name[i: i + 2]
        if len(sub) == 2:
            if sub in wrong_elements:
                return False
    return True


def generate_new_name(names, min_window=1):
    idx1 = 0
    idx2 = 0
    while idx1 == idx2:
        idx1 = np.random.randint(0, len(names) - 1)
        idx2 = np.random.randint(0, len(names) - 1)
    name1 = names[idx1]
    name2 = names[idx2]
    new_name1 = name1[0: np.random.randint(min_window, len(name1) - 1)]
    new_name2 = name2[np.random.randint(0, len(name2) - 1 - min_window):]
    new_name = new_name1 + new_name2
    return new_name.capitalize(), [name1.capitalize(), name2.capitalize()]


def get_wrong_elements():
    c_combinations = get_combinations(CONSTANTS)
    v_combinations = get_combinations(VOCALS)
    wrong_elements = c_combinations + v_combinations
    wrong_elements = ct.lists.delete_from_list(wrong_elements, CONSONANTIC_GROUP)
    return wrong_elements


def generate_cuchufletos_names(min_window=2,
                               ma_prob=0.15,
                               min_name_length=4,
                               min_last_name_length=6,
                               ):
    filedir = os.path.join(settings.DATA_PATH, 'names.toml')
    d = toml.load(filedir)
    names_prefixes = ['names_prefixes']
    names = d['names']
    last_names = d['last_names']
    wrong_elements = get_wrong_elements()
    while True:
        name, names_used = generate_new_name(names, min_window)
        last_name, last_names_used = generate_new_name(last_names, min_window)
        is_name = acceptable_name(name, wrong_elements, min_name_length) and acceptable_name(last_name, wrong_elements, min_last_name_length)
        if is_name:
            prefix = ct.lists.get_random_item(names_prefixes) + ' ' if np.random.uniform() <= ma_prob else ''
            final_name = f'{prefix}{name} {last_name}'
            break
    return final_name, names_used, last_names_used
