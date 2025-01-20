from fastapi import HTTPException, status

from src.api.business.models import Promo, Business, SubPromo, PromoCategory
from src.api.business.promo.schemas import PromoCreate
from src.db.deps import Session


def get_category(category_name: str, session: Session) -> PromoCategory:
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
        image_url=str(schema.image_url),
        age_from=schema.target.age_from,
        age_until=schema.target.age_until,
        country=schema.target.country.country if schema.target.country is not None else None,
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
        promos = []
        for uniq in schema.promo_unique:
            promos.append(SubPromo(promo_common=uniq, promo=promo))
        promo.promo_unique = promos
    else:
        if schema.promo_common is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        promo.promo_common = schema.promo_common

    session.add(promo)
    session.commit()
    session.refresh(promo)

    return promo
