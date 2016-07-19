# -*- coding: utf-8 -*-

__author__ = 'virtual'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Boolean, String, Integer, Sequence, Float, BigInteger
from sqlalchemy import ForeignKey, Numeric, TIMESTAMP, Date, DateTime, Time, desc, update, func
from sqlalchemy.orm import mapper, relationship, backref, relation


'''
    Схемы таблиц биллингов, используются для упрощения доступа к данным.

    Низкий уровень интерфейса.
'''


Base = declarative_base()

class BaseUtf8(Base):

    __tablename__ = 'dummy'

    dummy_id = Column(Integer, primary_key=True)

    def __getattr__(self, item):
        if type(item) == unicode:
            return item.encode('utf-8')
        else:
            return item
