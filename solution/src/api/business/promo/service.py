import datetime
import uuid

from fastapi import HTTPException, status

from src.api.business.models import Promo, Business, SubPromo, PromoCategory
from src.api.business.promo.schemas import PromoCreate, PromoResponse, Target, PromoEnum, PromosListSearchParams, \
    PromoPatch
from src.db.deps import Session


def get_category(category_name: str, session: Session) -> PromoCategory:
    category_name = category_name.lower()
    category = session.query(PromoCategory).filter(PromoCategory.name == category_name).first()
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
        if schema.promo_common is not None or schema.promo_unique is None:
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


def promo_to_response(promo: Promo) -> PromoResponse:
    base_data = to_promo_create(promo)
    return PromoResponse(
        **base_data.model_dump(exclude_unset=True),
        promo_id=str(promo.id),
        company_id=str(promo.business.id),
        company_name=promo.business.name,
        like_count=promo.like_count,
        used_count=promo.used_count,
        active=promo.active
    )


def get_promos_response_by_business_with_params(business: Business, params: PromosListSearchParams) -> list[
    PromoResponse]:
    if len(params.country) > 0:
        promos = [promo for promo in
                  filter(lambda p: p.country is None or p.country in params.country, business.promos)]
    else:
        promos = [promo for promo in business.promos]

    if params.sort_by is not None:
        if params.sort_by == "active_from":
            promos.sort(key=lambda p: p.active_from if p.active_from is not None else datetime.date.min, reverse=True)
        elif params.sort_by == "active_until":
            promos.sort(key=lambda p: p.active_until if p.active_until is not None else datetime.date.min, reverse=True)

    if params.offset is not None:
        promos[::] = promos[params.offset:]

    if params.limit is not None:
        promos[::] = promos[:params.limit]

    return [promo_to_response(promo) for promo in promos]


def update_promo(promo: Promo, schema: PromoPatch, session: Session) -> Promo:
    for param in schema.dict(exclude_unset=True):
        if param == "target":
            promo.age_from = None
            promo.age_until = None
            promo.country = None
            promo.categories.clear()

            for subparam in schema.target.dict(exclude_unset=True):
                setattr(promo, subparam, getattr(schema.target, subparam))
        else:
            setattr(promo, param, getattr(schema, param))

    session.commit()
    session.refresh(promo)
    return promo
