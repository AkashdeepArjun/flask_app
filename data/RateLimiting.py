from database import db
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String, Text, Numeric, Boolean
from decimal import Decimal


class RateLimiting(db.Model):

    __tablename__='request_rates'

    id:Mapped[int] = mapped_column(primary_key=True)
    ip:Mapped[str] = mapped_column(String(45),index=True)
    endpoint:Mapped[str] = mapped_column(String(100),index=True)
    timestamp: Mapped[datetime] = mapped_column(
      DateTime(timezone=True),
      default=lambda: datetime.now(timezone.utc),
      index=True,
  ) 

