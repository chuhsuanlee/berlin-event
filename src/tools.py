# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from config import SQLALCHEMY_URI, SQLALCHEMY_ECHO


# prepare session
engine = create_engine(SQLALCHEMY_URI, poolclass=QueuePool, echo=SQLALCHEMY_ECHO)
Session = sessionmaker(bind=engine)
session = Session()


def update_record(src, tar):
    for k in tar.__table__.columns.keys():
        if k not in ['id', 'created_at', 'updated_at'] and getattr(src, k) is not None:
            setattr(tar, k, getattr(src, k))
