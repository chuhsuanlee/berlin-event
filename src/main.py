# -*- coding: utf-8 -*-
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver

from model import Event
from tools import session, update_record
from config import WEB_SOURCE


def update_source_1():
    driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                              desired_capabilities=webdriver.DesiredCapabilities.CHROME)

    URL = 'https://www.deutscheoperberlin.de/en_EN/calendar'
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.quit()

    data = soup("ul", "month-container")
    for each_month in data:
        this_month = each_month.find("li", "month clearfix")
        try:
            month_string = this_month.span.string
        except AttributeError:
            month_string = this_month.string.strip()
        date = datetime.strptime(month_string, "%B %Y")
        for each_day in each_month("div", "cal__day__events-container clearfix"):
            date = date.replace(day=int(each_day.find("p", "cal__day__number").string))
            for each_event in each_day("div", "title cal__event__title clearfix"):
                record = Event(
                    web_source=1,
                    item_id=each_event.a['data-item-id'],
                    date=date,
                    title=each_event.a.string,
                )
                update_process(record)


def update_source_2():
    today = datetime.today()
    for i in xrange(3):
        month = today.month - 1 + i
        year = today.year + month // 12
        month = month % 12 + 1

        driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                  desired_capabilities=webdriver.DesiredCapabilities.CHROME)

        URL = 'https://gorki.de/en/programme/{}/{}/all'.format(year, month)
        driver.get(URL)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.quit()

        data = soup("h2", "h3")
        for each_event in data:
            url_string = each_event.a['href']
            time_string = url_string[url_string.rfind('/') + 1:]
            date = datetime.strptime(time_string, "%Y-%m-%d-%H%M")
            record = Event(
                web_source=2,
                item_id=time_string,
                date=date,
                title=each_event.a.string.strip(),
            )
            update_process(record)


def update_source_3():
    today = datetime.today()
    for i in xrange(3):
        month = today.month - 1 + i
        year = today.year + month // 12
        month = month % 12 + 1

        driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                  desired_capabilities=webdriver.DesiredCapabilities.CHROME)

        URL = 'http://berghain.de/events/{}-{}'.format(year, month)
        driver.get(URL)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.quit()

        stage_data = soup("h4", "type_stage")
        for each_event in stage_data:
            url_string = each_event.a['href']
            title_string = each_event.a['title']
            time_string = title_string[:title_string.find(':')]
            date = datetime.strptime(time_string, "%a %d %B %Y")
            record = Event(
                web_source=3,
                item_id=url_string[url_string.rfind('/') + 1:],
                date=date,
                title=title_string[title_string.find(':') + 2:],
            )
            update_process(record)

        dancefloor_data = soup("h4", "type_dancefloor")
        for each_event in dancefloor_data:
            url_string = each_event.a['href']
            title_string = each_event.a['title']
            time_string = title_string[:title_string.find(':')]
            date = datetime.strptime(time_string, "%a %d %B %Y")
            record = Event(
                web_source=3,
                item_id=url_string[url_string.rfind('/') + 1:],
                date=date,
                title=title_string[title_string.find(':') + 2:],
            )
            update_process(record)


def update_process(record):
    """Update the existed record or add new record."""
    record_matched = session.query(Event) \
                            .filter(Event.web_source == record.web_source) \
                            .filter(Event.item_id == record.item_id) \
                            .first()
    if record_matched:
        update_record(record, record_matched)
        session.commit()
    else:
        session.add(record)
        session.commit()


def choose_source(source_id):
    if source_id == 1:
        update_source_1()
    if source_id == 2:
        update_source_2()
    if source_id == 3:
        update_source_3()


if __name__ == "__main__":
    for i in [1, 2, 3]:
        print "Update {} events from {}".format(WEB_SOURCE[i][0], WEB_SOURCE[i][1])
        choose_source(i)
