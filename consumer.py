from scratch_1 import Article
from datetime import datetime
import json
import sched
import time
import os
import shutil
from os import walk

_I = 0
_LOG_FILE = f'./log1/deserialize-log-{datetime.now().strftime("%Y_%m_%d")}.txt'
_PATH_DOWN = "json/"
_PATH_DST = "json/loaded"
_PATH_ERR = "json/error"


def log(s):
    with open(_LOG_FILE, "a") as f:
        f.write(f'{datetime.now().isoformat()} | {s} \n')


def main():
    log("START")
    print("--- start ---")
    s = sched.scheduler(time.time, time.sleep)
    s.enter(3, 1, do_work, (s,))
    s.run()
    print("---start---")
    log("STOP")


def do_work(s: sched.scheduler):
    global _I
    print(f'---{_I}---')
    wath_dir(_PATH_DOWN)
    _I = _I + 1
    s.enter(3, 1, do_work, (s,))


def wath_dir(path):
    file_names = next(walk(path), (None, None, []))[2]
    for file_name in file_names:
        log(f'обнаружен файл {file_name}')
        try:
            art_dict = read_file(_PATH_DOWN, file_name)
            article = Article.from_dict(art_dict)
            copy_file(file_name)
            log(f'{_I}Объект восстановлен {article}')
            print_article(article)
        except Exception as err:
            log(f'ОШИБКА - {err}')
            error_copy_file(file_name)
        finally:
           remove_file(file_name)


def read_file(path, f_name):
    with open(f'{path}{f_name}', "r") as f:
        art_dict = json.load(f)
        return art_dict


def copy_file(f_name):
    shutil.copy(f'{_PATH_DOWN}{f_name}', _PATH_DST)


def error_copy_file(f_name):
    shutil.copy(f'{_PATH_DOWN}{f_name}', _PATH_ERR)


def remove_file(f_name):
    os.remove(f'{_PATH_DOWN}{f_name}')


def print_article(art: Article):
    print(art.title, art.body, art.like, art.datetime)
    log(f'Данные обработаны!')


if __name__ == '__main__':
    main()
