# -*- coding: utf-8 -*-

__author__ = 'virtual'

from .. import Smart
from schema.smart.acct.payments import Payments
from schema.smart.core.payments import Payments as CPayments
from schema.smart.acct.payment_types import PaymentTypes
from sqlalchemy.sql import func
from schema.smart.acct.bills import Bills as SBills
from schema.smart.acct.bill_items import BillItems
from schema.smart.core.charge_groups import ChargeGroups
from config.diff_params import *
from datetime import datetime


class Bills(Smart):

    def __init__(self, session):
        Smart.__init__(self, session)

    def get_payments(self, params={}):
        q = self.session.query(
            Payments

            #.operator_name.label('Operator'),
            #Payments.pay_date.label('Date'),
            #Payments.paymenttype_id.label('NType'),
            #Payments.amount_rur.label('Summa'),
            #Payments.account_num.label('Count')
        )
        #q = q.join(PaymentTypes)
        q = self.get_parametrized_filter(Payments, q, params)
        return q.all()

    def insert_payment(self, payment, acc_num):
        profile = 'ttk'
        params = {
            'account_num': acc_num,
            'pay_date': payment.mdate,
            'provider_company_id': provider_bcid_map_r[payment.bcid],
            'type': payment_types_r[profile][payment.ntype]['type'],
            'paymenttype_id': payment_types_r[profile][payment.ntype]['payment_type_id'],
            'operator_name': (payment.operator.name).encode('utf-8'),
            'status': 0,
            'amount_rur': payment.amount,
            'extract_date': payment.mdate,
            'loaded': 1,
        }
        q = self.session.query(Payments)
        q = self.get_parametrized_filter(Payments, q, params)
        pays = q.all()

        if len(pays) > 0:
            print pays
            #return None
            for pay in pays:
                print pay
                self.process_payment(pay, params)

        else:
            nparams = params
            nparams.update({
                'create_date': datetime.now(),
                'description': 'From Onyma TTK',
            })
            pay = Payments()
            for param in params:
                if param in pay.__dict__:
                    pay.__dict__[param] = params[param]

            print pay

            self.session.add(pay)
            self.session.commit()
            q = self.session.query(Payments)
            q = self.get_parametrized_filter(Payments, q, params)
            npays = q.all()
            for npay in npays:
                self.process_payment(npay, nparams)

    def fill_core_payment(self, payment):
        cpay = CPayments()
        cpay.acct_pid = payment.id
        cpay.create_date = payment.create_date
        cpay.extract_date = payment.extract_date
        cpay.payment_date = payment.pay_date
        cpay.type = payment.ntype
        cpay.paymenttype_id = payment.paymenttype_id

    def process_payment(self, payment, params):
        cparams = {
            'acct_id': payment.id,
        }
        q = self.session.query(CPayments)
        q = self.get_parametrized_filter(CPayments, q, cparams)
        cpays = q.all()
        if len(cpays) == 0:
            cpay = self.fill_core_payment(payment)
            self.session.add(cpay)
            self.session.commit()
        else:
            for cpay in cpays:
                for param in params:
                    if param in cpay.__dict__:
                        cpay.__dict__[param] = params[param]


    def get_bills(self, params={}):
        q = self.session.query(
            SBills
        )
        q = q.join(BillItems)
        q = self.get_parametrized_filter(SBills, q, params)
        return q.all()

    def get_charges(self, params={}):
        q = self.session.query(ChargeGroups)
        q = self.get_parametrized_filter(ChargeGroups, q, params)
        return q.all()

    def get_balance(self, account):

        return 0

    def get_payments_group(self, params={}):
        q = self.session.query(
            Payments.operator_name.label('Operator'),
            Payments.pay_date.label('Date'),
            Payments.paymenttype_id.label('NType'),
            func.sum(Payments.amount_rur).label('Summa'),
            func.count(Payments.amount_rur).label('Count')
        )
        #q = q.join(PaymentTypes)
        q = self.get_parametrized_filter(Payments, q, params)
        q = q.group_by(Payments.operator_name, Payments.pay_date, Payments.paymenttype_id)
        q = q.order_by(Payments.pay_date)
        return q.all()

    def get_bills_group(self, params={}):
        q = self.session.query(
            Payments.operator_name.label('Operator'),
            Payments.pay_date.label('Date'),
            Payments.paymenttype_id.label('NType'),
            func.sum(Payments.amount_rur).label('Summa'),
            func.count(Payments.amount_rur).label('Count')
        )
        #q = q.join(PaymentTypes)
        q = self.get_parametrized_filter(Payments, q, params)
        q = q.group_by(Payments.operator_name, Payments.pay_date, Payments.paymenttype_id)
        q = q.order_by(Payments.pay_date)
        return q.all()
