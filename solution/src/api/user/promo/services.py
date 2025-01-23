"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "fusion" by Rapid Integration (https://github.com/rapid-integration).
Available at: https://github.com/rapid-integration/fusion

This code may be based on "api" by Quotepedia (https://github.com/quotepedia).
Available at: https://github.com/quotepedia/api

Modifications made by Danila Sedelnikov on January 2025.
"""

from src.api.business.models import Promo
from src.api.user.models import User
from src.db.deps import Session


def add_like_to_promo_by_user(user: User, promo: Promo, session: Session):
    if user not in promo.user_likes:
        promo.user_likes.add(user)
        session.commit()
        session.refresh(promo)
        session.refresh(user)


def delete_like_to_promo_by_user(user: User, promo: Promo, session: Session):
    if user in promo.user_likes:
        promo.user_likes.remove(user)
        session.commit()
        session.refresh(promo)
        session.refresh(user)
