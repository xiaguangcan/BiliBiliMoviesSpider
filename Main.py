# -*- coding: utf-8 -*-
from BiliBiliSpider import *
import Sqlite3Util

category_list = (
    '剧情', '喜剧', '爱情', '美国', '恐怖', '经典', '动作', '悬疑', '科幻', '奇幻', '冒险', '战争', '神作', '文艺', '搞笑', '法国', '青春', '英国', '治愈向',
    '萝莉')


def get_different_category_movies(max_page_num, category):
    bili_spider = BiliBiliSpider()

    while bili_spider.page <= max_page_num:
        movies_list = bili_spider.driver_bilibili(category)
        Sqlite3Util.create_bili_table()
        for item in movies_list:
            if Sqlite3Util.check_movie_exist(item.bili_movies_url):
                Sqlite3Util.update_bili_movies(item)
            else:
                Sqlite3Util.insert_bili_movies(item)
        bili_spider.page += 1


if __name__ == '__main__':
    global category_list
    get_different_category_movies(5, category_list[0])
    Sqlite3Util.close_db()
