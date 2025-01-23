"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "fusion" by Rapid Integration (https://github.com/rapid-integration).
Available at: https://github.com/rapid-integration/fusion

This code may be based on "api" by Quotepedia (https://github.com/quotepedia).
Available at: https://github.com/quotepedia/api

Modifications made by Danila Sedelnikov on January 2025.
"""
from sqlalchemy import and_, or_, func

from src.api.business.models import Promo
from src.api.business.promo.service import get_category, is_promo_is_active_on_cur_date
from src.api.user.feed.schemas import PromoToUserSearchParams, PromoForUser
from src.api.user.models import User
from src.db.deps import Session


def promo_to_response_for_user(promo: Promo, user: User, session: Session) -> PromoForUser:
    return PromoForUser(
        promo_id=str(promo.id),
        company_id=str(promo.business_id),
        company_name=promo.business.name,
        description=promo.description,
        image_url=str(promo.image_url) if promo.image_url is not None else None,
        active=is_promo_is_active_on_cur_date(promo, session),
        is_activated_by_user=True if user in promo.user_activates else False,
        like_count=len(promo.user_likes),
        is_liked_by_user=True if user in promo.user_likes else False,
        #     TODO убрать заглушку
        comment_count=0
    )


def get_promos_response_to_user_with_params(user: User, query: PromoToUserSearchParams, session: Session) -> (list[
                                                                                                                  PromoForUser],
                                                                                                              int):
    promos = session.query(Promo)

    promos = promos.filter(
        or_(
            and_(Promo.country.is_(None)),
            and_(func.lower(Promo.country) == func.lower(user.country))
        )
    )

    promos = promos.filter(
        or_(
            and_(Promo.age_from <= user.age, Promo.age_until >= user.age),
            and_(Promo.age_from.is_(None), Promo.age_until.is_(None)),
            and_(Promo.age_from.is_(None), Promo.age_until >= user.age),
            and_(Promo.age_until.is_(None), Promo.age_from <= user.age)
        )
    )

    if query.category is not None:
        user_category = get_category(query.category, session)
        promos.filter(Promo in user_category.promos)

    if query.active is not None:
        promos = promos.filter(Promo.active == query.active)

    promos = promos.all()
    promos.sort(lambda p: p.created_at, reverse=True)

    total_count = len(promos)

    if query.offset is not None:
        promos[::] = promos[query.offset:]

    if query.limit is not None:
        promos[::] = promos[:query.limit]

    return [promo_to_response_for_user(promo, user, session) for promo in promos], total_count
