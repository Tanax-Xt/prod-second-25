"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "fusion" by Rapid Integration (https://github.com/rapid-integration).
Available at: https://github.com/rapid-integration/fusion

This code may be based on "api" by Quotepedia (https://github.com/quotepedia).
Available at: https://github.com/quotepedia/api

Modifications made by Danila Sedelnikov on January 2025.
"""

from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy.orm import Session as __Session

from src.db import ENGINE


def __get_session() -> Generator[__Session, None, None]:
    session = __Session(ENGINE)
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


Session = Annotated[__Session, Depends(__get_session)]
