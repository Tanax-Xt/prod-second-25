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

from fastapi import HTTPException, status
from sqlalchemy import func

from src.api.business.models import Business, Promo, SubPromo, PromoCategory, PromoActivateToUser
from src.api.business.promo.schemas import PromoCreate, PromoResponse, Target, PromoEnum, PromosListSearchParams, \
    PromoPatch, PromoStat, CountryStat
from src.db.deps import Session


def get_category(category_name: str, session: Session) -> PromoCategory:
    category_name = category_name
    category = session.query(PromoCategory).filter(func.lower(PromoCategory.name) == func.lower(category_name)).first()
    if category is None:
        category = PromoCategory(name=category_name)
        session.add(category)
        session.commit()
        session.refresh(category)
    return category


def create_promo(session: Session, schema: PromoCreate, business: Business) -> Promo:
    promo = Promo(
        description=schema.description,
        image_url=str(schema.image_url) if schema.image_url is not None else None,
        age_from=schema.target.age_from,
        age_until=schema.target.age_until,
        country=schema.target.country,
        max_count=schema.max_count,
        active_from=schema.active_from,
        active_until=schema.active_until,
        mode=schema.mode.upper(),
        business=business
    )

    if schema.target.categories is not None:
        for category_name in schema.target.categories:
            category = get_category(category_name, session)
            promo.categories.append(category)

    if schema.mode == "UNIQUE":
        if schema.promo_common is not None or schema.promo_unique is None or schema.max_count != 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        promos = []
        for uniq in schema.promo_unique:
            promos.append(SubPromo(promo_common=uniq, promo=promo))
        promo.promo_unique = promos
    else:
        if schema.promo_common is None or schema.promo_unique is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        promo.promo_common = schema.promo_common

    session.add(promo)
    session.commit()
    session.refresh(promo)

    return promo


def get_promo_by_id(promo_id: uuid.UUID, session: Session) -> Promo:
    return session.query(Promo).filter(Promo.id == promo_id).first()


def get_active_subpromo_by_promo_id(promo_id: uuid.UUID, session: Session) -> list[SubPromo]:
    return session.query(SubPromo).filter(((SubPromo.promo_id == promo_id) & (SubPromo.active == True))).all()


def to_promo_create(promo: Promo) -> PromoCreate:
    return PromoCreate(
        description=promo.description,
        target=Target(
            age_from=promo.age_from,
            age_until=promo.age_until,
            country=promo.country,
            categories=[c.name for c in promo.categories] if promo.categories else None
        ),
        image_url=promo.image_url,
        max_count=promo.max_count,
        active_from=promo.active_from,
        active_until=promo.active_until,
        mode=PromoEnum(promo.mode),
        promo_common=promo.promo_common,
        promo_unique=[sp.promo_common for sp in promo.promo_unique] if promo.promo_unique else None
    )


def promo_to_response(promo: Promo, session: Session) -> PromoResponse:
    base_data = to_promo_create(promo)
    return PromoResponse(
        **base_data.model_dump(exclude_unset=True),
        promo_id=str(promo.id),
        company_id=str(promo.business.id),
        company_name=promo.business.name,
        like_count=len(promo.user_likes),
        used_count=len(promo.user_activates),
        active=is_promo_is_active_on_cur_date(promo, session)
    )


def get_promos_response_by_business_with_params(business: Business, params: PromosListSearchParams,
                                                session: Session) -> (list[
                                                                          PromoResponse],
                                                                      int):
    if len(params.country) > 0:
        promos = [promo for promo in
                  filter(lambda p: p.country is None or p.country.lower() in params.country, business.promos)]
    else:
        promos = [promo for promo in business.promos]

    if params.sort_by is not None:
        if params.sort_by == "active_from":
            promos.sort(key=lambda p: p.active_from if p.active_from is not None else datetime.date.max, reverse=True)
        elif params.sort_by == "active_until":
            promos.sort(key=lambda p: p.active_until if p.active_until is not None else datetime.date.max, reverse=True)
    else:
        promos.sort(key=lambda p: p.created_at, reverse=True)

    total_count = len(promos)

    if params.offset is not None:
        promos[::] = promos[params.offset:]

    if params.limit is not None:
        promos[::] = promos[:params.limit]

    return [promo_to_response(promo, session) for promo in promos], total_count


def update_promo(promo: Promo, schema: PromoPatch, session: Session) -> Promo:
    if promo.mode == "UNIQUE" and schema.max_count != 1:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    if promo.mode == "COMMON" and schema.max_count < promo.used_count:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    if promo.mode == "COMMON" and schema.max_count == promo.used_count and promo.active:
        promo.active = False

    if promo.mode == "COMMON" and schema.max_count >= promo.used_count and not promo.active:
        promo.active = True


    for param in schema.dict(exclude_unset=True):
        if param == "target":
            promo.age_from = None
            promo.age_until = None
            promo.country = None
            promo.categories.clear()

            for subparam in schema.target.dict(exclude_unset=True):
                if subparam == "categories":
                    for category in schema.target.categories:
                        promo.categories.append(get_category(category, session))
                else:
                    setattr(promo, subparam, getattr(schema.target, subparam))
        elif param == "image_url":
            setattr(promo, param, str(getattr(schema, param)))
        else:
            setattr(promo, param, getattr(schema, param))

    session.commit()
    session.refresh(promo)
    return promo


def is_validate_age(age_from: int, age_until: int) -> bool:
    if age_from is not None and age_until is not None:
        return age_from <= age_until
    return True


def is_validate_date(age_from: datetime.date, age_until: datetime.date) -> bool:
    if age_from is not None and age_until is not None:
        return age_from <= age_until
    return True


def is_promo_is_active_on_cur_date(promo: Promo, session: Session) -> bool:
    if promo.active is False:
        return False

    active = (promo.active_from is None or promo.active_from <= datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=3))).date()) and (
                     promo.active_until is None or promo.active_until >= datetime.datetime.now(
                 datetime.timezone(datetime.timedelta(hours=3))).date())

    if promo.active is not active:
        promo.active = active

        session.commit()
        session.refresh(promo)

    return active


def get_stat_for_promo(promo: Promo, session: Session) -> PromoStat:
    stat = PromoStat()

    activations = session.query(PromoActivateToUser).filter(PromoActivateToUser.promo_id == promo.id)
    stat.activations_count = activations.count()

    countries = {}

    for user in promo.user_activates:
        c = user.country.lower()
        if c in countries:
            countries[c] += activations.filter(PromoActivateToUser.user_id == user.id).count()
        else:
            countries[c] = activations.filter(PromoActivateToUser.user_id == user.id).count()

    if len(countries) > 0:
        stat.countries = []

    for country in sorted(countries.keys()):
        stat.countries.append(CountryStat(country=country, activations_count=countries[country]))

    return stat
