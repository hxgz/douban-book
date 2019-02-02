#! coding:utf-8

import re

from bs4 import BeautifulSoup

from easyHTTP.client import API


class DoubanAPIBase(API):
    HOST = "https://api.douban.com/"

    @classmethod
    def _wrap_book(cls, item):
        return {
            'id': item['id'],
            'title': item['title'],
            'title2': item['origin_title'],
            'img': item['image'],
            'rate': item['rating']['average'],
            'rate_sample': item['rating']['numRaters'],
            'author_list': item['author'],
            'publish_list': [item['publisher']],
            'pubdate': item['pubdate'],
            'tag_list': [t['title'] for t in item['tags']],
            'translator_list': item['translator'],
            'page': item['pages'] or '',
            "summary": item['summary'],
            "author_summary": item['author_intro'],
            'binding': item['binding'],
            'price': item['price'],
            'catalog_list': item['catalog'].split('\t')
        }


class DoubanBookSearch(DoubanAPIBase):
    PATH = "v2/book/search"

    def transform(self, data):
        return {
            "start": data['start'],
            "count": data['count'],
            "total": data['total'],
            "book_list": [
                self._wrap_book(item) for item in data['books']]
        }


class DoubanBookInfo(DoubanAPIBase):
    PATH = "v2/book/{book_id}"

    def transform(self, data):
        return self._wrap_book(data)


class DoubanTop250(API):
    HOST = "https://book.douban.com/"
    PATH = "top250"

    def transform(self, data):
        book_list = []

        soup = BeautifulSoup(data)
        for book_soup in soup.find_all(name='tr', attrs={"class": "item"}):
            book = {}

            title_soup = book_soup.find(name="div", attrs={"class": "pl2"})
            book['id'] = re.match(r'.*subject/([0-9]*)/', title_soup.a['href'], re.S).group(1)
            book['title'] = title_soup.a.getText(strip=True)
            book['title2'] = title_soup.span.getText(strip=True) if title_soup.span else ''

            book['img'] = book_soup.img['src']

            info = book_soup.find(name="p", attrs={"class": "pl"}).getText(strip=True).split(' / ')

            book['author_list'] = info[0:-3]
            book['publish_list'] = info[-3].split(' ')
            book['pubdate'] = info[-2]
            book['price'] = info[-1]

            rate_soup = book_soup.find(name="div", attrs={"class": "star"})
            book['rate'] = rate_soup.find(name="span", attrs={"class": "rating_nums"}).getText()

            m = re.match(r".+?([0-9]+)",
                         rate_soup.find(name="span", attrs={"class": "pl"}).getText(strip=True),
                         re.S)
            book['rate_sample'] = m.group(1)

            suggest_soup = book_soup.find(name="span", attrs={"class": "inq"})
            book['suggest'] = suggest_soup.getText(strip=True) if suggest_soup else ""

            book_list.append(book)

        return book_list


class DoubanMobileBase(API):
    HOST = "https://m.douban.com/"

    def get_headers(self):
        return {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "Referer": "https://m.douban.com/"
        }

    def transform(self, data):
        return {
            "start": data['start'],
            "count": data['count'],
            "total": data['total'],
            "book_list": [{
                'id': item['id'],
                'title': item['title'],
                'title2':'',
                'img':item['cover']['url'],
                'rate': item['rating']['value'] if item['rating'] else 0,
                'rate_sample':item['rating']['count'] if item['rating'] else 0,
                'author_list': item['author'],
                'publish_list': item['press'],
                'pubdate': item['year'][0],
                'suggest': item.get('recommend_comment', '')
            }for item in data['subject_collection_items']]
        }


class DoubanHotBooks(DoubanMobileBase):
    PATH = "/rexxar/api/v2/subject_collection/book_{book_type}/items"


class DoubanWeeklyHotBooks(DoubanMobileBase):
    PATH = "/rexxar/api/v2/subject_collection/book_{book_type}_hot_weekly/items"


class DoubanBook(object):

    async def search_book(self, search_text, start=0, count=20):
        """搜书
        """
        params = {
            "q": search_text,
            "start": start,
            "count": count,
        }
        return await DoubanBookSearch().call(params=params)

    async def hot_books(self, book_type="nonfiction", start=0, count=20):
        """受关注图书 （非虚构，虚构）
        :param book_type nonfiction非虚构, fiction虚构
        """
        params = {
            "os": "ios",
            "for_mobile": 1,
            "start": start,
            "count": count,
            "loc_id": 0,
            "_": 0
        }

        path_args = {
            "book_type": book_type
        }
        return await DoubanHotBooks().call(path_args=path_args, params=params)

    async def weekly_hot_books(self, book_type="nonfiction", start=0, count=10):
        """受关注图书 （非虚构，虚构）
        :param book_type nonfiction非虚构, fiction虚构
        """
        params = {
            "start": start,
            "count": count,
        }

        path_args = {
            "book_type": book_type
        }
        return await DoubanWeeklyHotBooks().call(path_args=path_args, params=params)

    async def top250(self, start=0):
        '''豆瓣图书 Top 250
        每页25本
        https://book.douban.com/top250?start=0
        '''

        return {
            "start": start,
            "count": 25,
            "total": 250,
            "book_list": await DoubanTop250().call(params={'start': start})
        }

    async def get_book(self, book_id):
        path_args = {"book_id": book_id}
        return await DoubanBookInfo().call(path_args=path_args)


#import asyncio
#db = DoubanBook()
#asyncio.get_event_loop().run_until_complete(
#    # db.top250()
#    # db.get_book(1770782)
#    # db.hot_books()
#    db.hot_books(book_type="nonfiction", start=0, count=10)
#    # db.search_book("马伯庸")
#    # db.get_book(11534920)
#    #db.weekly_hot_books(book_type='fiction', start=9)
#)
