# -*- coding: utf-8 -*-

WEB_SOURCE = {
    0: ("C/O Berlin", "https://www.co-berlin.org/en/calender"),
    1: ("Deutsche Oper Berlin", "https://www.deutscheoperberlin.de/en_EN/calendar"),
    2: ("GORKI", "https://gorki.de/en/programme"),
    3: ("Berghain Berlin", "http://berghain.de/events/"),
}

SQLALCHEMY_URI = '{driver}://{user}:{pwd}@{host}/{db}?charset=utf8' \
    .format(
        driver='mysql+pymysql',
        host='127.0.0.1:3306',
        user='root',
        pwd='0000',
        db='chuhsuanlee'
    )
SQLALCHEMY_ECHO = False
