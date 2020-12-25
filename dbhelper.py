"""
This file contains the schema design for the database tables.
For the purpose of this project the database contains only two tables.
The transactions table and the address table.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from sqlalchemy import Column, Float, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker

ENGINE = create_engine('sqlite:///ripple.db', echo=True)
BASE = declarative_base()
SESSION = sessionmaker(bind=ENGINE)


class TransactionObject(BASE):
    __tablename__ = 'Transactions'

    id = Column(Integer, primary_key=True)  # Auto increment primary key
    transaction_hash = Column(String)  # Hash of the specific transaction

    transaction_time = Column(String)  # Time when transaction took place
    transaction_type = Column(String)  # Type of transaction. For this project just the "Payment"

    amount_value = Column(Float)  # Transaction amount sent by the account
    amount_currency = Column(String)  # The currency of the transaction amount by the account

    transaction_result = Column(String)  # Whether it is success or failed ( Path dry )

    delivered_amount = Column(Float)  # Transaction delivered amount . Usually less than teh amount
    delivered_currency = Column(String)  # Which currency the receiver received it

    account = Column(String)  # The origin of the transaction
    destination = Column(String)  # The destination of the transaction


    def __init__(self, _hash, _time, _a_val, _a_currency, _tx_res,
                 _d_amount, _d_currency, _accnt, _dest):
        self.transaction_hash = _hash
        self.transaction_time = _time
        self.amount_value = _a_val
        self.amount_currency = _a_currency
        self.transaction_result = _tx_res
        self.delivered_amount = _d_amount
        self.delivered_currency = _d_currency
        self.account = _accnt
        self.destination = _dest
        self.transaction_type = 'Payment'

    def __repr__(self):
        return "<Tx hash: {0}, Tx time: {1}, Tx acc: {2}, Tx dest: {3}, Tx  delivered: {4}, " \
               "Tx delivered currency: {5}".format(self.transaction_hash, self.transaction_time,
                                                   self.account, self.destination, self.delivered_amount,
                                                   self.delivered_currency)


class AddressNode(BASE):
    __tablename__ = 'AddressNode'

    id = Column(Integer, primary_key=True)
    address = Column(String)
    incoming_nodes = Column(Integer)
    outgoing_nodes = Column(Integer)


def add_tx_obj(o_list):
    session = SESSION()
    session.add_all(o_list)
    session.commit()


def add_addr_obj(addr_list):
    session = SESSION()
    session.add_all(addr_list)
    session.commit()
    session.close()


def getSession():
    """
    Please whenever you make this call, make sure to close the resulting object, so that you do not
    overrun the whole db
    :return: The session obj to interact with the db.
    """
    return SESSION()


if __name__ == '__main__':
    BASE.metadata.create_all(ENGINE)
