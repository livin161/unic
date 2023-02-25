import random
from datetime import datetime


class Article:

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.datetime = datetime.now().strftime("%Y_%m_%d_%H-%M-%S")
        self.like = random.randint(10, 100)

    def to_dict(o: object):
        res = o.__dict__
        res["class"] = o.__class__.__name__
        return res

    def from_dict(o: dict):
            art = Article(o["title"], o["body"])
            art.like = o["like"]
            art.datetime = o["datetime"]
            return art