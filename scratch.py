from urllib.request import *
from bs4 import BeautifulSoup
from tool import *
from time import sleep
import hashlib
from mysql.connector import *
import re

# explored_num = 0
# max_num = 10


class Book:
    def __init__(self, name, score, url):
        self.id = re.findall('\d+', url)[0]
        self.name = name
        self.score = score
        self.url = url


class AllBook:
    def __init__(self):
        self.booknum = 0
        self.max_booknum = 20
        self.min_score = 11


def book_score(soup):
    tag = soup.find('strong')
    if tag:
        score = text_in_tag(tag)
        score = score.strip()
        if score:
            score = float(score)
            return score
    return None

def text_in_tag(tag):
    return tag.string.encode().decode()


def book_name(soup):
    tag = soup.find('title')
    title = text_in_tag(tag)
    name = title[:-5]
    name = name.strip()
    return name


def more_books(soup):
    a_tags = a_tags_with_bookdata(soup)
    books = list()
    for a in a_tags:
        name = text_in_tag(a)
        name = name.strip()
        score = None
        url = a.attrs['href']
        b = Book(name, score, url)
        books.append(b)
    return books

def a_tags_with_bookdata(soup):
    imgs_tags = soup.find_all('img', 'm_sub_img')
    a_tags = list()
    for img in imgs_tags:
        a = img.parent
        dt = a.parent
        line_break_char = dt.next_sibling
        dd = line_break_char.next_sibling
        line_break_char = dd.next_element
        a = line_break_char.next_sibling
        a_tags.append(a)
    return a_tags

def handle_book(allbook, book, conn, cursor):
    insert_book(allbook, book, conn, cursor)
    if allbook.booknum > allbook.max_booknum:
        remove_book(allbook, conn, cursor)
    update_min_score(allbook, cursor)


def can_insert(allbook, book):
    if book.score:
        if book.score > allbook.min_score \
                or allbook.booknum < allbook.max_booknum:
            return True
    else:
        return False


def is_higher_score(allbook, book):
    return book.score > allbook.min_score


def insert_book(allbook, book, conn, cursor):
    allbook.booknum += 1
    insert_book_db(book, conn, cursor)

def insert_book_db(book, conn, cursor):
    insert_sql = "INSERT INTO book(id, name, score) " \
                 "VALUES (%s, %s, %s);"
    values = [book.id, book.name, book.score]
    cursor.execute(insert_sql, values)
    conn.commit()

def insert_explored_url(book, conn, cursor):
    insert_sql = "INSERT INTO explored_book(id, name)" \
                 "VALUES (%s, %s);"
    [id] = re.findall('\d+', book.url)
    name = book.name
    values = [id, name]
    cursor.execute(insert_sql, values)
    conn.commit()

def remove_book(allbook, conn, cursor):
    allbook.booknum -= 1
    remove_book_db(allbook, conn, cursor)

def remove_book_db(allbook, conn, cursor):
    delete_sql = "delete from book " \
                 "where score = %s " \
                 "limit 1;"
    values = [allbook.min_score]
    cursor.execute(delete_sql, values)
    conn.commit()


def update_min_score(allbook, cursor):
    select_sql = "select min(score) from book;"
    cursor.execute(select_sql)
    for (score,) in cursor:
        allbook.min_score = score


def explore_book(allbook, book, conn, cursor):
    insert_explored_url(book, conn, cursor)

    # global explored_num, max_num
    with urlopen(book.url) as response:
        soup = BeautifulSoup(response, 'lxml')

        book.score = book_score(soup)
        print(book.name, book.score, book.url)

        if can_insert(allbook, book):
            handle_book(allbook, book, conn, cursor)
        books = more_books(soup)

        for b in books:
            if not is_explored(b.url, cursor):
                # if (explored_num < max_num):
                #     explored_num += 1
                explore_book(allbook, b, conn, cursor)

def is_explored(url, cursor):
    book_id = re.findall('\d+', url)
    query_sql = "select id " \
                "from explored_book " \
                "where id = %s " \
                "limit 1;"
    values = book_id
    cursor.execute(query_sql, values)

    for (book_id_, ) in cursor:
        return True
    return False

def connect_db():
    conn = connect(
        user='latin',
        password='123',
        host='localhost',
        database='Scratch'
        )
    cursor = conn.cursor()
    return conn, cursor


def __main():
    conn, cursor = connect_db()
    init_db(cursor)

    allbook = AllBook()
    url = 'https://book.douban.com/subject/1390650/'
    start_explore(allbook, url, conn, cursor)

def init_db(cursor):
    truncate_sql = "truncate book"
    cursor.execute(truncate_sql)
    truncate_sql = "truncate explored_book"
    cursor.execute(truncate_sql)



def start_explore(allbook, url, conn, cursor):
    # global explored_num, max_num
    sleep(1)
    with urlopen(url) as response:
        soup = BeautifulSoup(response, 'lxml')
        name = book_name(soup)
        score = book_score(soup)
        book = Book(name, score, url)

        insert_book(allbook, book, conn, cursor)
        # 没有score的页面也可以访问more_books的页面
        if name:
            books = more_books(soup)
            for b in books:
                if not is_explored(url, cursor):
                    # if (explored_num < max_num):
                    #     explored_num += 1
                    explore_book(allbook, b, conn, cursor)


__main()
