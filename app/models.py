from database import Base
from sqlalchemy import (
    TIMESTAMP,
    Column,
    Integer,
    String,
    text,
    ForeignKey,
    Float,
)


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    city = Column(String, nullable=False)
    phone_no = Column(String, nullable=False)


class Accounts(Base):
    __tablename__ = "accounts"
    account_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    cash_balance = Column(Float, nullable=False)
    bank_balance = Column(Float, nullable=False)
    total_balance = Column(Float, nullable=False)
    investable_balance = Column(Float, nullable=False)


class Transactions(Base):
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    account_type = Column(String, nullable=False)
    category = Column(String, nullable=False)
    timestamp = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Investable(Base):
    __tablename__ = "investable"
    investable_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    investable_percent = Column(Integer, nullable=False)


class Stocks(Base):
    __tablename__ = "stocks"
    stock_id = Column(Integer, primary_key=True, nullable=False)
    symbol = Column(String, nullable=False)
    sector = Column(String, nullable=False)
    ltp = Column(Float, nullable=False)
    pe = Column(Float, nullable=False)
    pb = Column(Float, nullable=False)
    roe = Column(Float, nullable=False)
    roa = Column(Float, nullable=False)
