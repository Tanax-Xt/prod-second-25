from sqlalchemy import create_engine

from src.config import settings
from src.db.models import Base

ENGINE = create_engine(str(settings.POSTGRES_URI))


