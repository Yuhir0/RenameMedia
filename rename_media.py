import sys
import subprocess
import re
import os

from datetime import datetime


CODE_PATH = os.path.dirname(sys.modules[__name__].__file__)
print(CODE_PATH)
LOG_FILE = sys.modules[__name__].__file__.replace('.py', '.log')
loging = None
CHAPTER_METADATA = '.last_chap'

REPLACEMENTS = (
    (r'\[[^\]]+\]', ''),
    (r'\([^\)]+\)', ''),
    (r'^\s+', ''),
    (r'\s+\.', '.'),
    (r'-', ''),
    (r'\s\s', ' '),
)

only_chapter_pattern = r'\-\s+(\d+).*(\.\w+)$'
extension_pattern = r'\.\w+$'

chapter_pattern = r's*\-\s+(\d+)'
season_pattern = r'season\s?(\d+)'

args_dict = dict(
    name='',
    path='./',
    all='no',
    title=''
)

conf_params = dict()


def log(text):
    loging.write(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]: {text}\n')


def get_args(*args):
    for arg in args:
        name, val = arg.split('=')
        if (not name in args_dict):
            raise Exception(f'Unkown argument "{name}"')
        args_dict[name] = val


def replacement_name(name):
    search = re.search(only_chapter_pattern, name)
    return search.group(1) + search.group(2)


def get_season_from_path(path):
    search = re.search(season_pattern, path, flags=re.IGNORECASE)	
    if search:
        return search.group(1)
    return conf_params.get('season', '01')


def get_season(path):
    return str(conf_params.get('season', '01') if \
        conf_params.get('force_config', False) \
        else get_season_from_path(path)).zfill(2)


def store_chap_metadata(path, chap):
    with open(os.path.join(path, CHAPTER_METADATA), 'w') as metadata:
        metadata.write(chap)


def get_next_chapter(path):
    full_path = os.path.join(path, CHAPTER_METADATA)
    chap = None
    if os.path.exists(full_path):
        with open(full_path, 'r') as metadata:
            meta = metadata.read()
            if meta:
                chap = str(int(meta) + 1)
    if not chap:
        chap = str(conf_params.get('first_chap', '01'))
    store_chap_metadata(path, chap)
    return chap


def get_chap_and_ext_from_name(name, path):
    search = re.search(only_chapter_pattern, name)
    if search:
        chap = get_next_chapter(path) if conf_params.get('sequencial', False) else search.group(1)
        ext = search.group(2)
        store_chap_metadata(path, chap)
        return chap, ext
    else:
        return get_next_chapter(path), '.mkv'


def get_title():
    return conf_params.get('title', '') if \
         not args_dict['title'] or conf_params.get('force_config', False) \
         else args_dict['title']


def replace_name(name, path):
    log(f'name -> {name}')
    season = get_season(path)
    log(f'season -> {season}')
    chap, ext = get_chap_and_ext_from_name(name, path)
    log(f'chap -> {chap}')
    new_name = name
    if args_dict["title"]:
        title = get_title()
        new_name = f'{title} S{season} E{chap.zfill(2)}{ext}'
    else:
        for pattern, replacement in REPLACEMENTS:
            new_name = re.sub(pattern, replacement, new_name)
        new_name = re.sub(chapter_pattern, f'S{season} E{chap}', new_name)

    log(f'new_name -> {new_name}')
    full_path = os.path.join(path, name)
    new_full_path = os.path.join(path, new_name)
    os.rename(full_path, new_full_path)


def load_title_config(path):
    conf_path = os.path.join(path, '.title_conf.yml')
    if os.path.exists(conf_path):
        with open(conf_path) as ymlfile:
            confp = yaml.load(ymlfile, yaml.loader.Loader)
        conf_params.update(confp)
        log(f'title conf -> {conf_params}')


def dir_sort_filter(item):
    for rep in REPLACEMENTS:
        item = re.sub(rep[0], rep[1], item)
    return item


def replace_all_files_in_path(path):
    ls_dir = os.listdir(path)
    ls_dir.sort(key=dir_sort_filter)
    for _file in ls_dir:
        if not _file.startswith('.') \
            and os.path.isfile(os.path.join(path, _file)):
            replace_name(_file, path)


def main(*args):
    get_args(*args)
    log(args_dict)
    load_title_config(args_dict['path'])
    if args_dict['all'].lower() == 'yes':
        replace_all_files_in_path(args_dict['path'])
    else:
        replace_name(args_dict['name'], args_dict['path'])


if __name__ == '__main__':
    loging = open(LOG_FILE, 'a')
    try:
        subprocess.check_output(['pip3', 'install', '-r', os.path.join(CODE_PATH, '.requirements')])

        # Import requirements
        import yaml

        main(*sys.argv[1:])
    except Exception as e:
        print(f'Execution filed!! - {e}')
        log(f'ERROR - {e}')
    loging.close()
