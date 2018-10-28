# -*- coding: utf-8 -*-
from datetime import datetime

from bs4 import BeautifulSoup
# from pandas import DataFrame
from selenium import webdriver

from model import Event
from tools import session, update_record


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


if __name__ == "__main__":
    update_source_1()
