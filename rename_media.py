import sys
from datetime import datetime
import re
import os


LOG_FILE = f"./{sys.modules[__name__].__file__.replace('.py', '')}.log"
loging = None

REPLACEMENTS = (
    (r'\[[^\]]+\]', ''),
    (r'\([^\)]+\)', ''),
    (r'^\s+', ''),
    (r'\s+\.', '.'),
)

only_chapter_pattern = r'\-\s+(\d+).*(\.\w+)$'
sequencial_file_pattern = r'^\d+\.\w+$'
extension_pattern = r'\.\w+$'

chapter_pattern = r's*\-\s+(\d+)'
season_pattern = r'season\s?(\d+)'

args_dict = dict(
    name='',
    path='./',
    sequencial='no',
    all='no',
    title=''
)


def log(text):
    loging.write(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]: {text}\n')


def get_args(*args):
    for arg in args:
        name, val = arg.split('=')
        if (not name in args_dict):
            raise Exception(f'Unkown argument "{name}"')
        args_dict[name] = val


def secuancial_name(name, path):
    files = [_file for _file in os.listdir(path) if re.match(sequencial_file_pattern, _file) and os.path.isfile(os.path.join(path, _file))]
    log(files)
    extension = search = re.search(only_chapter_pattern, name).group(2)
    if (not files):
        return '1' + extension
    else:
        files.sort(reverse=True)
        previous_file = re.sub(extension_pattern, '', files[0])
        log(previous_file)
        return str(int(previous_file) + 1) + extension


def replacement_name(name):
    search = re.search(only_chapter_pattern, name)
    return search.group(1) + search.group(2)


def get_season_from_path(path):
    search = re.search(season_pattern, path, flags=re.IGNORECASE)	
    if search:
        return search.group(1)
    return '01'


def get_replacements(name):
    log(CUSTOM_REPLACE)
    for key, custom in CUSTOM_REPLACE.items():
        log(f'custom -> {key}')
        if key in name:
            return value + REPLACEMENTS
    return REPLACEMENTS


def get_chap_and_ext_from_name(name):
    search = re.search(only_chapter_pattern, name)
    if search:
        return search.group(1), search.group(2)
    else:
        return '××'


def replace_name(name, path, sequencial=False):
    log(f'name -> {name}')
    season = get_season_from_path(path)
    log(f'season -> {season}')
    chap, ext = get_chap_and_ext_from_name(name)
    log(f'chap -> {chap}')
    new_name = name
    if args_dict["title"]:
        new_name = f'{args_dict["title"]} S{season} E{chap}{ext}'
    else:
        for pattern, replacement in get_replacements(name):
            new_name = re.sub(pattern, replacement, new_name)
        """
        if sequencial:
            new_name = secuancial_name(name, path)
        else:
            new_name = replacement_name(name)
        """
        new_name = re.sub(chapter_pattern, f'S{season} E{chap}', new_name)
    log(f'new_name -> {new_name}')
    os.rename(path + name, path + new_name)


def replace_all_files_in_path(path):
    for _file in os.listdir(path):
        if os.path.isfile(os.path.join(path, _file)):
            replace_name(_file, path)


def main(*args):
    get_args(*args)
    log(args_dict)
    if args_dict['all'].lower() == 'yes':
        replace_all_files_in_path(args_dict['path'])
    else:
        replace_name(args_dict['name'], args_dict['path'], args_dict['sequencial'].lower() == 'yes')


if __name__ == '__main__':
    loging = open(LOG_FILE, 'a')
    try:
        main(*sys.argv[1:])
    except Exception as e:
        print(f'Execution filed!! - {e}')
        log(f'ERROR - {e}')
    loging.close()
