from database import insert_book_db, remove_book_db, min_score


def is_target_book(allbook, book):
    if book.score:
        if book.score > allbook.min_score \
                or allbook.booknum < allbook.max_booknum:
            return True
    else:
        return False

def update_allbook(allbook, book, conn, cursor):
    insert_book(allbook, book, conn, cursor)
    if allbook.booknum > allbook.max_booknum:
        remove_book(allbook, conn, cursor)
    update_min_score(allbook, cursor)

def insert_book(allbook, book, conn, cursor):
    allbook.booknum += 1
    insert_book_db(book, conn, cursor)

def remove_book(allbook, conn, cursor):
    allbook.booknum -= 1
    remove_book_db(allbook, conn, cursor)

def update_min_score(allbook, cursor):
    allbook.min_score = min_score(cursor)
