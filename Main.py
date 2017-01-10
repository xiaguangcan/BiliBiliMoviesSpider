# -*- coding: utf-8 -*-
from BiliBiliSpider import *
import Sqlite3Util

if __name__ == '__main__':

    bili_spider = BiliBiliSpider()
    movies_list = bili_spider.driver_bilibili('动作')
    Sqlite3Util.create_bili_table()
    for item in movies_list:
        if Sqlite3Util.check_movie_exist(item.bili_movies_url):
            Sqlite3Util.update_bili_movies(item)
        else:
            Sqlite3Util.insert_bili_movies(item)

    Sqlite3Util.close_db()
