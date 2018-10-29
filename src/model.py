# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    web_source = Column(Integer)
    item_id = Column(String(45))
    date = Column(DateTime)
    title = Column(String(255))
    updated_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
