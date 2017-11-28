from urllib.request import *
from bs4 import BeautifulSoup
from book import Book


def get_soup(url):
    with urlopen(url) as response:
        soup = BeautifulSoup(response, 'lxml')
        return soup

def get_book(soup, url):
    score = book_score(soup)
    name = book_name(soup)
    b = Book(name, score, url)
    return b

def book_score(soup):
    tag = soup.find('strong')
    if tag:
        score = text_in_tag(tag)
        score = score.strip()
        if score:
            score = float(score)
            return score
    return None

def book_name(soup):
    tag = soup.find('title')
    title = text_in_tag(tag)
    name = title[:-5]
    name = name.strip()
    return name

def urls_for_more_books(soup):
    imgs_tags = soup.find_all('img', 'm_sub_img')
    urls = list()
    for img in imgs_tags:
        a = img.parent
        url = a.attrs['href']
        urls.append(url)
    return urls

def text_in_tag(tag):
    return tag.string.encode().decode()


# def a_tags_with_bookdata(soup):
#     imgs_tags = soup.find_all('img', 'm_sub_img')
#     a_tags = list()
#     for img in imgs_tags:
#         a = img.parent
#         dt = a.parent
#         line_break_char = dt.next_sibling
#         dd = line_break_char.next_sibling
#         line_break_char = dd.next_element
#         a = line_break_char.next_sibling
#         a_tags.append(a)
#     return a_tags
