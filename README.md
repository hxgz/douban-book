# douban-book
douban book API

豆瓣book相关api

## install

beautifulsoup4
easyHTTP (https://github.com/hxgz/easyHTTP)

python setup.py install

## 简单使用例子

```python
from douban_book.book import DoubanBook
await DoubanBook().get_book(11534920)
```

## api

**get_book**
获取豆瓣书籍信息

`book_id` 豆瓣书籍id

**search_book**
搜书  
`search_text ` 书籍，作者  
`start` 0 下标  
`count` 每页数  

**hot_books**
受关注图书 （非虚构，虚构）

`book_type` nonfiction 非虚构(默认)，fiction虚构
`start`, `count`

**weekly_hot_books**
每周受关注图书 （非虚构，虚构）

`book_type` nonfiction 非虚构(默认)，fiction虚构
`start`, `count`

**top250**
豆瓣图书 top250

`start`  
豆瓣每页返回25本  



## 使用同步调用例子

```python
import asyncio
from douban_book.book import DoubanBook

db = DoubanBook()
asyncio.get_event_loop().run_until_complete(
    # db.top250()
    # db.get_book(1770782)
    # db.hot_books()
    # db.search_book("马伯庸")
    # db.get_book(11534920)
    #db.weekly_hot_books(book_type='fiction', start=9)
)

```
