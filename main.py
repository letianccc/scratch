from book import *
from handle_allbook import *
from soup import get_book, get_soup, urls_for_more_books
from database import connect_db, init_db, not_explored, insert_explored_book
from time import sleep

def __main():
    conn, cursor = connect_db()
    init_db(cursor)

    allbook = AllBook()
    start_url = 'https://book.douban.com/subject/1390650/'
    explore_book(allbook, start_url, conn, cursor)

def explore_book(allbook, url, conn, cursor):
    sleep(1)
    soup = get_soup(url)
    book = get_book(soup, url)
    print(book.name, book.score, book.url)
    insert_explored_book(book, conn, cursor)

    if is_target_book(allbook, book):
        update_allbook(allbook, book, conn, cursor)

    urls = urls_for_more_books(soup)
    for url in urls:
        if not_explored(url, cursor):
            explore_book(allbook, url, conn, cursor)


__main()
