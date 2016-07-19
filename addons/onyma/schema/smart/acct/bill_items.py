# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
from .bills import Bills

class BillItems(Base):
    __tablename__ = 'bill_items'

    __table_args__ = {'extend_existing': True, 'schema':'acct', }

    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey('acct.bills.id'))
    num = Column(Integer)
    name = Column(String)
    quantitytype = Column(String)
    object_name = Column(String)
    amount = Column(Float)
    price = Column(Float)
    total = Column(Float)
    vat_rate = Column(Float)
    service_type = Column(Integer)
    service_sub_type = Column(Integer)

    start_date = Column(DateTime)
    end_date = Column(DateTime)

    user_service_sub_type = Column(String)
    order_name = Column(String)

    bill = relationship(Bills, primaryjoin=(bill_id == Bills.id)) #, remote_side='account_number', backref='payments')

    def __repr__(self):
        return "[%s:%d] %s %f %f" % (
            self.bill.num,
            self.num,
            self.name,
            self.amount,
            self.total,
        )
