import uuid
from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models import Base


class Business(Base):
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(index=True, unique=True)
    password: Mapped[str] = mapped_column()

    promos: Mapped[list["Promo"]] = relationship(back_populates="business")


class PromoToCategory(Base):
    promo_id: Mapped[int] = mapped_column(ForeignKey("promo.id", ondelete="CASCADE"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("promo_category.id", ondelete="CASCADE"), primary_key=True)


class SubPromo(Base):
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    promo_common: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column(default=True)

    promo_id: Mapped[str] = mapped_column(ForeignKey("promo.id", ondelete="SET NULL"), default=None)
    promo: Mapped["Promo"] = relationship(back_populates="promo_unique")


class PromoCategory(Base):
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(unique=True, index=True)

    promos: Mapped[list["Promo"]] = relationship(back_populates="categories", secondary="promo_to_category")


class Promo(Base):
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    description: Mapped[str] = mapped_column()
    image_url: Mapped[Optional[str]] = mapped_column()
    age_from: Mapped[Optional[int]] = mapped_column()
    age_until: Mapped[Optional[int]] = mapped_column()
    country: Mapped[Optional[str]] = mapped_column()
    max_count: Mapped[int] = mapped_column()
    active_from: Mapped[Optional[date]] = mapped_column()
    active_until: Mapped[Optional[date]] = mapped_column()
    mode: Mapped[str] = mapped_column()
    promo_common: Mapped[Optional[str]] = mapped_column()
    active: Mapped[bool] = mapped_column(default=True)

    categories: Mapped[Optional[list["PromoCategory"]]] = relationship(back_populates="promos",
                                                                       secondary="promo_to_category")
    promo_unique: Mapped[Optional[list["SubPromo"]]] = relationship(back_populates="promo")

    business_id: Mapped[str] = mapped_column(ForeignKey("business.id", ondelete="SET NULL"), default=None)
    business: Mapped["Business"] = relationship(back_populates="promos")

    like_count: Mapped[int] = mapped_column(default=0)
    used_count: Mapped[int] = mapped_column(default=0)
