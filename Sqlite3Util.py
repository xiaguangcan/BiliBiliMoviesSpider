# -*- coding: utf-8 -*-
import os
import sqlite3

spiders_connect = None


def get_db_connect():
    global spiders_connect

    if not os.path.exists(os.path.dirname(os.path.abspath("__file__")) + '\db'):
        os.makedirs('db')

    if spiders_connect is None:
        spiders_connect = sqlite3.connect(os.path.dirname(os.path.abspath("__file__")) + '\db\spiders.db')
    return spiders_connect


def create_bili_table():
    db_connect = get_db_connect()
    db_connect.execute(
        "CREATE TABLE IF NOT EXISTS 'bili_movies'('bili_movies_id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,'bili_movies_name' VARCHAR(100) NOT NULL,'bili_movies_url' VARCHAR(200) NOT NULL,'bili_movies_des' TEXT,'bili_movies_play_num' INT(11) NOT NULL DEFAULT '0','bili_movies_img' VARCHAR(200) DEFAULT NULL,'bili_movies_category' VARCHAR(20) NOT NULL DEFAULT '综合');")
    db_connect.execute("CREATE INDEX IF NOT EXISTS idx_bili_name ON 'bili_movies'('bili_movies_name');")


def insert_bili_movies(movies_info):
    db_connect = get_db_connect()
    db_connect.text_factory = str
    parameter = (movies_info.bili_movies_name, movies_info.bili_movies_url, movies_info.bili_movies_des,
                 movies_info.bili_movies_play_num,
                 movies_info.bili_movies_img, movies_info.bili_movies_category)
    db_connect.execute(
        'INSERT INTO bili_movies(bili_movies_name,bili_movies_url,bili_movies_des,bili_movies_play_num,bili_movies_img,bili_movies_category) VALUES (?,?,?,?,?,?);',
        parameter)


def update_bili_movies(movies_info):
    db_connect = get_db_connect()
    db_connect.text_factory = str
    parameter = (movies_info.bili_movies_name, movies_info.bili_movies_url, movies_info.bili_movies_des,
                 movies_info.bili_movies_play_num,
                 movies_info.bili_movies_img, movies_info.bili_movies_category)
    db_connect.execute(
        'UPDATE bili_movies SET bili_movies_name=?,bili_movies_des=?,bili_movies_play_num=?,bili_movies_img=?, bili_movies_category=? WHERE bili_movies_url=?;',
        parameter)


def check_movie_exist(bili_movies_url):
    db_connect = get_db_connect()
    cursor = db_connect.execute('SELECT * FROM bili_movies WHERE bili_movies_url=?', (bili_movies_url,))
    if cursor is not None:
        content = cursor.fetchone()
        if content is not None:
            return True
        else:
            return False


def close_db():
    global spiders_connect

    if spiders_connect is not None:
        spiders_connect.commit()
        spiders_connect.close()
        spiders_connect = None
