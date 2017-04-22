# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
import requests
import sys

default_image_url = '/img/image_not_found.png'
default_description = 'No information or still in retrieving...'

reload(sys)
sys.setdefaultencoding('utf8')


class IMDBInfoHTMLParser(HTMLParser):
    global default_image_url, default_description
    img_tag = False
    desc_tag = False
    poster_img = default_image_url
    description = default_description

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if len(attrs) > 0:
                if attrs[0][0] == 'class' and attrs[0][1] == 'poster':
                    self.img_tag = True
                elif attrs[0][0] == 'class' and attrs[0][1] == 'summary_text':
                    self.desc_tag = True
        elif self.img_tag is True and tag == 'img':
            for name, value in attrs:
                if name == 'src':
                    self.poster_img = value
                    self.img_tag = False

    def handle_endtag(self, tag):
        if tag == 'div':
            self.img_tag = False
            self.desc_tag = False

    def get_img(self):
        return self.poster_img

    def handle_data(self, data):
        if self.desc_tag is True:
            self.summary_text = data.strip()
            self.desc_tag = False

    def get_description(self):
        return self.summary_text


class IMDBUrlHTMLParser(HTMLParser):
    got_tag = False
    movie_url = None
    find_count = 0
    base_url = 'http://www.imdb.com'

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            if len(attrs) > 0 and attrs[0][0] == 'class' and attrs[0][1] == 'findList':
                self.got_tag = True
        elif self.got_tag is True and self.find_count == 0 and tag == 'a':
            # return the first movie url from search result
            for name, value in attrs:
                if name == 'href':
                    self.movie_url = self.base_url + value
                    self.find_count += 1
                    self.got_tag = False

    def handle_endtag(self, tag):
        if tag == 'table':
            self.got_tag = False

    def get_movie_url(self):
        return self.movie_url


def get_movie_extra_infomation(url=None):
    if url is None or url.strip() == "":
        return default_image_url, default_description
    """
    get url real url
    if url start with http://www.imdb.com/title/, find poster url from content
    if url start with http://www.imdb.com/find, find first find movie url than get its poster
    """
    image_url = default_image_url
    description = default_description
    r = requests.get(url)
    if r.url.startswith('http://www.imdb.com/title/'):
        parser = IMDBInfoHTMLParser()
        parser.feed(r.content)
        image_url = parser.get_img()
        description = parser.get_description()
    elif r.url.startswith('http://www.imdb.com/find'):
        parser = IMDBUrlHTMLParser()
        parser.feed(r.content)
        new_url = parser.get_movie_url()
        if new_url is not None:
            r = requests.get(new_url)
            parser = IMDBInfoHTMLParser()
            parser.feed(r.content)
            image_url = parser.get_img()
            description = parser.get_description()
    return image_url, description
