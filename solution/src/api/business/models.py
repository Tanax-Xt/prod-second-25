
from sqlalchemy.orm import Mapped, mapped_column, relationship

from solution.src.db.models import Base


class Business(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    password: Mapped[str] = mapped_column()
    # avatar_url: Mapped[str | None] = mapped_column(nullable=True)
    #
    # bills: Mapped[list["Bill"]] = relationship(back_populates="to_user", cascade="all")
    # groups: Mapped[list["Group"]] = relationship(secondary="group_user", back_populates="users")
    # created_groups: Mapped[list["Group"]] = relationship(back_populates="created_by_user", cascade="all")
    # transactions: Mapped[list["Transaction"]] = relationship(back_populates="from_user", cascade="all")
