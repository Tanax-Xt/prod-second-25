"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "fusion" by Rapid Integration (https://github.com/rapid-integration).
Available at: https://github.com/rapid-integration/fusion

This code may be based on "api" by Quotepedia (https://github.com/quotepedia).
Available at: https://github.com/quotepedia/api

Modifications made by Danila Sedelnikov on January 2025.
"""

import json
from datetime import datetime

import requests
from sqlalchemy import desc

from src.api.business.models import Promo, PromoActivateToUser
from src.api.business.promo.service import get_active_subpromo_by_promo_id, get_promo_by_id
from src.api.service import get_secret, set_secret_with_timedelta
from src.api.user.models import User
from src.api.user.promo.comments.schemas import CommentsToUserSearchParams
from src.config import settings
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


def is_correct_country(user: User, promo: Promo) -> bool:
    return promo.country is None or (promo.country.lower() == user.country.lower())


def is_correct_age(user: User, promo: Promo) -> bool:
    return (promo.age_from is None and promo.age_until is None) or \
        (promo.age_from is None and user.age <= promo.age_until) or \
        (promo.age_from <= user.age and promo.age_until is None) or \
        (promo.age_from <= user.age <= promo.age_until)


def is_user_fits_to_target(user: User, promo: Promo) -> bool:
    return is_correct_country(user, promo) and is_correct_age(user, promo)


def is_correct_antifraud_status(user: User, promo: Promo) -> bool:
    ok = get_secret(user.email, settings.ANTIFRAUD_SECRET_PREFIX)

    if ok is not None:
        return bool(ok)

    response = requests.post(
        f"http://{settings.ANTIFRAUD_ADDRESS}/api/validate",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"user_email": user.email, "promo_id": str(promo.id)})
    )

    if response.status_code != 200:
        return False

    result = response.json()

    if "cache_until" in result:
        cache_until_dt = datetime.fromisoformat(result["cache_until"][:-1]) - datetime.utcnow()
        set_secret_with_timedelta(user.email, str(int(result["ok"])), settings.ANTIFRAUD_SECRET_PREFIX, cache_until_dt)

    if result["ok"] is False:
        return False
    return True


def get_promo_var(user: User, promo: Promo, session: Session) -> str | None:
    if promo.mode == "COMMON":
        if promo.max_count <= promo.used_count:
            return None
        promo.user_activates.append(user)
        promo.used_count += 1

        if promo.used_count == promo.max_count:
            promo.active = False

        session.commit()
        session.refresh(promo)
        return promo.promo_common
    else:
        subpromos = get_active_subpromo_by_promo_id(promo.id, session)

        if len(subpromos) == 0:
            return None

        promo.user_activates.append(user)
        subpromo = subpromos.pop()

        if len(subpromos) == 0:
            promo.active = False
            session.commit()
            session.refresh(promo)

        subpromo.active = False
        session.commit()
        session.refresh(subpromo)
        return subpromo.promo_common


def get_user_activations_history(user: User, session: Session, query: CommentsToUserSearchParams) -> (list[Promo], int):
    promos = session.query(PromoActivateToUser).filter(PromoActivateToUser.user_id == user.id).order_by(
        desc(PromoActivateToUser.created_at))

    total_count = len(promos.all())

    promos = promos.limit(query.limit)

    if query.offset is not None:
        promos = promos.offset(query.offset)

    promos = [get_promo_by_id(promo.promo_id, session) for promo in promos.all()]

    return promos, total_count
