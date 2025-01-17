from sqlalchemy import create_engine

from solution.src.config import settings
from solution.src.db.models import Base

ENGINE = create_engine(str(settings.POSTGRES_URI))


