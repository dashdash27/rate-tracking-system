from datetime import datetime
from typing import List
from decimal import Decimal
from sqlalchemy import Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class RequestLog(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    status_code: Mapped[int] = mapped_column(Integer)
    base_currency: Mapped[str] = mapped_column(String(3), default="USD")

    # связь с таблицей rates
    rates: Mapped[List["CurrencyRate"]] = relationship(back_populates="request")

class CurrencyRate(Base):
    __tablename__ = "rates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("requests.id"))
    currency_code: Mapped[str] = mapped_column(String(3))
    value: Mapped[Decimal] = mapped_column(Numeric(10, 4))

    # обратная связь с request
    request: Mapped["RequestLog"] = relationship(back_populates="rates")