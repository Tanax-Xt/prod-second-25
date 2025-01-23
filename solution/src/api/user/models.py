"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "fusion" by Rapid Integration (https://github.com/rapid-integration).
Available at: https://github.com/rapid-integration/fusion

This code may be based on "api" by Quotepedia (https://github.com/quotepedia).
Available at: https://github.com/quotepedia/api

Modifications made by Danila Sedelnikov on January 2025.
"""
import datetime
import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.mixin import AuditMixin
from src.db.models import Base

if TYPE_CHECKING:
    from src.api.business.models import Promo


class User(Base):
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    password: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    image_url: Mapped[Optional[str]] = mapped_column()
    age: Mapped[int] = mapped_column()
    country: Mapped[str] = mapped_column()

    promo_likes: Mapped[Optional[set["Promo"]]] = relationship(back_populates="user_likes",
                                                               secondary="promo_like_to_user")

    promo_activates: Mapped[Optional[set["Promo"]]] = relationship(back_populates="user_activates",
                                                                   secondary="promo_activate_to_user")

    comments: Mapped[Optional[list["Comment"]]] = relationship(back_populates="author")


class Comment(Base, AuditMixin):
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text: Mapped[str] = mapped_column()

    author_id: Mapped[str] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"), default=None)
    author: Mapped["User"] = relationship(back_populates="comments")

    promo_id: Mapped[str] = mapped_column(ForeignKey("promo.id", ondelete="SET NULL"), default=None)
    promo: Mapped["Promo"] = relationship(back_populates="comments")
