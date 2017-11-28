from mysql.connector import *
import re

def connect_db():
    conn = connect(
        user='latin',
        password='123',
        host='localhost',
        database='Scratch'
        )
    cursor = conn.cursor()
    return conn, cursor

def init_db(cursor):
    truncate_sql = "truncate book;"
    cursor.execute(truncate_sql)
    truncate_sql = "truncate explored_book;"
    cursor.execute(truncate_sql)

def not_explored(url, cursor):
    book_id = re.findall('\d+', url)[0]
    query_sql = "select id from explored_book" \
                " where id = %s " \
                " limit 1;"
    values = [book_id]
    cursor.execute(query_sql, values)
    for book_id_ in cursor:
        return False
    return True

def insert_book_db(book, conn, cursor):
    insert_sql = "INSERT INTO book(id, name, score) " \
                 "VALUES (%s, %s, %s);"
    values = [book.id, book.name, book.score]
    cursor.execute(insert_sql, values)
    conn.commit()

def remove_book_db(allbook, conn, cursor):
    delete_sql = "delete from book " \
                 "where score = %s " \
                 "limit 1;"
    values = [allbook.min_score]
    cursor.execute(delete_sql, values)
    conn.commit()

def insert_explored_book(book, conn, cursor):
    insert_sql = "INSERT INTO explored_book(id, name)" \
                 " VALUES (%s, %s);"
    id = re.findall('\d+', book.url)[0]
    name = book.name
    values = [id, name]
    cursor.execute(insert_sql, values)
    conn.commit()

def min_score(cursor):
    select_sql = "select min(score) from book;"
    cursor.execute(select_sql)
    for (score,) in cursor:
        return score
