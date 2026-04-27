from sqlalchemy import Index, String, Integer, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infra.db.base import (
    Base, UUIDMixin, TimestampMixin
)

class Plan(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "plans"
    __table_args__ = (
        UniqueConstraint("tier", "billing_interval", name="uq_plan_tier_interval"),
        Index("ix_plans_tier", "tier")
    )
    
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    tier: Mapped[]