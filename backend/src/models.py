from venv import create
from sqlalchemy import Column,ForeignKey, Integer, Table
from sqlalchemy.types import Integer, Text, String
from sqlalchemy.types import Integer, Text, String, DateTime,Float
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship
from connector import Connector
from config import Config
from sqlalchemy.ext.declarative import DeclarativeMeta
import json

Base = declarative_base()




class User(Base):


    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    username = Column(String(255), unique=True, nullable=False)
    # password = Column(Text, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    # first_name = Column(String(255))
    # last_name = Column(String(255))
    # bio = Column(Text)
    # avatar_url = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    groups = relationship("Group")

    def __repr__(self):
        return f"<User {self.username}>"



class Group(Base):


    __tablename__ = "group"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    group_name = Column(String(255), nullable=False)
    created_by = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<User {self.username}>"



class UserGroup(Base):
    

    __tablename__ = "usergroup"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("group.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<User {self.username}>"



class Expense(Base):
    

    __tablename__ = "expense"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    expense_name = Column(String(255), unique=True, nullable=False)
    amount = Column(Float)
    group_id = Column(Integer, ForeignKey("group.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    # expense_splits = relationship("ExpenseSplit", back_populates="expense")
    # children = relationship("ExpenseSplit", back_populates="parent")
    children = relationship("ExpenseSplit", backref="parent")

    def __repr__(self):
        return f"<User {self.username}>"



class ExpenseSplit(Base):


    __tablename__ = "expensesplit"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    expense_id = Column(Integer, ForeignKey("expense.id"), nullable=False)
    payee_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    share_amount = Column(Float)
    pending_amount = Column(Float)
    payer_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    # expense = relationship("Expense", back_populates="expense_splits")
    # parent = relationship("Expense", back_populates="children")

    def __repr__(self):
        return f"<Payer {self.payer_id}, Payee {self.payee_id}, Pending amount {self.pending_amount}>"



class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)



def create_all_models():
    connector = Connector(Config.DB_ENDPOINT)
    # session = connector.db_session
    engine = connector.db_engine
    Base.metadata.create_all(engine)




