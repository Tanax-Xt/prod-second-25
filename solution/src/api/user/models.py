import uuid
from typing import Optional

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models import Base


class User(Base):
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    password: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    image_url: Mapped[Optional[str]] = mapped_column()
    age: Mapped[int] = mapped_column()
    country: Mapped[str] = mapped_column()
