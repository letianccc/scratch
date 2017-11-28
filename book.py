import re

class AllBook:
    def __init__(self):
        self.booknum = 0
        self.max_booknum = 20
        self.min_score = 11
        
class Book:
    def __init__(self, name, score, url):
        self.id = re.findall('\d+', url)[0]
        self.name = name
        self.score = score
        self.url = url
