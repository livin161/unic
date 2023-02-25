import json
import random
from datetime import datetime
import time
import sched
import pickle
from scratch_1 import Article


_I = 0
_J = 0
_LOG_FILE = f'./log1/serialize-log-{datetime.now().strftime("%Y_%m_%d")}.txt'
_TIME_SEC = 5


def main():
    set_sched()


def log(s: str):
    with open(_LOG_FILE, "a") as f:
        f.write(f'{datetime.now().isoformat()} | {s} \n')


def send_json_data(art: Article):
    global _I
    _I = _I + 1
    try:
        fd = f'json/{_I}-{datetime.now().strftime("%Y_%m_%d_%H-%M-%S")}-data.json'
        with open(fd, "x") as f:
            json.dump(art, f, default=Article.to_dict)
    except AttributeError as err:
        log(f'ошибка - {_J} - {err}')
    except Exception as err:
        log(f'ошибка - {_I} - {err}')
    finally:
        print("finally")


def send_pickles(art: Article):
    global _I
    _I = _I + 1
    try:
        fd = f'pickle/{_I}-{datetime.now().strftime("%Y_%m_%d_%H-%M-%S")}-data.pickle'
        with open(fd, 'wb') as f:
            pickle.dump(art, f, protocol=pickle.HIGHEST_PROTOCOL)
    except AttributeError as err:
        log(f'ошибка - {_J} - {err}')
    except Exception as err:
        log(f'ошибка - {_I} - {err}')
    finally:
        print("finally")


def set_sched():
    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, do_work, (s, ))
    s.run()


def do_work(s: sched.scheduler):
    global _J
    _J = _J + 1
    log("-start-")
    print(f'--- {_J} ---')
    art = Article(f'Title - {random.randint(10, 100)}', "BODY TEST WEIGHT")
    print(art.title, art.body)
    send_json_data(art)
    send_pickles(art)
    s.enter(_TIME_SEC, 1, do_work, (s,))
    log("-stop-")


if __name__ == '__main__':
    main()