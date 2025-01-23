"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "fusion" by Rapid Integration (https://github.com/rapid-integration).
Available at: https://github.com/rapid-integration/fusion

This code may be based on "api" by Quotepedia (https://github.com/quotepedia).
Available at: https://github.com/quotepedia/api

Modifications made by Danila Sedelnikov on January 2025.
"""

import uuid
from datetime import date
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.mixin import AuditMixin
from src.db.models import Base

if TYPE_CHECKING:
    from src.api.user.models import User, Comment


class Business(Base):
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(index=True, unique=True)
    password: Mapped[str] = mapped_column()

    promos: Mapped[list["Promo"]] = relationship(back_populates="business")


class PromoToCategory(Base):
    promo_id: Mapped[str] = mapped_column(ForeignKey("promo.id", ondelete="CASCADE"), primary_key=True)
    category_id: Mapped[str] = mapped_column(ForeignKey("promo_category.id", ondelete="CASCADE"), primary_key=True)


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


class PromoLikeToUser(Base):
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    promo_id: Mapped[str] = mapped_column(ForeignKey("promo.id", ondelete="CASCADE"), primary_key=True)


class PromoActivateToUser(Base):
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    promo_id: Mapped[str] = mapped_column(ForeignKey("promo.id", ondelete="CASCADE"), primary_key=True)


class Promo(Base, AuditMixin):
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

    user_likes: Mapped[Optional[set["User"]]] = relationship(back_populates="promo_likes",
                                                             secondary="promo_like_to_user")

    user_activates: Mapped[Optional[set["User"]]] = relationship(back_populates="promo_activates",
                                                                 secondary="promo_activate_to_user")
    used_count: Mapped[int] = mapped_column(default=0)

    comments: Mapped[Optional[list["Comment"]]] = relationship(back_populates="promo")
