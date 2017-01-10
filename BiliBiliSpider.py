# -*- coding:utf-8 -*-
import logging
import urllib2

import lxml.html
import gzip
import StringIO
from selenium import webdriver
from BiliMoviesInfo import *

logging.basicConfig(level=logging.INFO)


class BiliBiliSpider:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64)', 'Content-Type': 'text/html; charset=UTF-8',
                        'Accept-Encoding': 'gzip, deflate, sdch'}
        self.page = 1
        self.html_url = 'http://www.bilibili.com/video/movie_west_1.html#!page=' + str(
            self.page) + '&tagid=6716&tag=%E5%8A%A8%E4%BD%9C'

    def get_html_content(self):
        request = urllib2.Request(self.html_url, None, self.headers)
        response = urllib2.urlopen(request)
        if response.info().get('Content-Encoding') == 'gzip':
            response_content = self.unzip(response)
            return response_content
        else:
            response_content = response.read().decode('utf-8')
            return response_content

    def parse_html_content(self, html_content):
        html_fromstring = lxml.html.fromstring(html_content)
        print html_fromstring

    def unzip(self, response):
        buf = StringIO.StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        html = f.read()
        return html

    def driver_bilibili(self, category):
        movies_list = []

        driver = webdriver.Chrome()
        driver.get('http://www.bilibili.com/video/movie_west_1.html#!page=' + str(
            self.page) + '&tagid=6716&tag=' + category)
        print driver.page_source
        driver_movies_list = driver.find_elements_by_xpath('//div[@class="l-item"]')
        for item in driver_movies_list:
            try:
                driver_left_movie_path_name = item.find_element_by_xpath('./div[@class="l-l"]/a[last()]')
                movie_url = driver_left_movie_path_name.get_attribute('href')
                driver_left_movie_img = item.find_element_by_xpath('./div[@class="l-l"]/a[1]//img')
                left_movie_img_url = driver_left_movie_img.get_attribute('src')
                if movie_url is not None:
                    movie_name = driver_left_movie_path_name.text
                    driver_right_movie_desc = item.find_element_by_xpath('./div[@class="l-r"]/div[@class="v-desc"]')
                    right_movie_desc = driver_right_movie_desc.text
                    driver_right_movie_play = item.find_element_by_xpath(
                        './div[@class="l-r"]/div[@class="v-info"]/span[@class="v-info-i gk"]/span')
                    right_movie_play_num = driver_right_movie_play.text
                    movies_info = MoviesInfo(movie_name, movie_url, right_movie_desc, right_movie_play_num,
                                             left_movie_img_url,category)
                    movies_list.append(movies_info)
            except Exception:
                print movie_url
        return movies_list
