from src.api.business.models import Promo, Business, SubPromo, PromoCategory
from src.api.business.promo.schemas import PromoCreate
from src.db.deps import Session


def create_promo(session: Session, schema: PromoCreate, business: Business) -> Promo:
    promo = Promo(
        description=schema.description.description,
        image_url=str(schema.image_url.image_url),
        age_from=schema.target.age_from,
        age_until=schema.target.age_until,
        country=schema.target.country.country,
        max_count=schema.max_count,
        active_from=schema.active_from,
        active_until=schema.active_until,
        mode=schema.mode.upper(),
        business=business
    )

    for category in schema.target.categories:
        promo.categories.append(PromoCategory(name=category))

    if schema.mode == "UNIQUE":
        promos = []
        for uniq in schema.promo_unique:
            promos.append(SubPromo(promo_common=uniq, promo=promo))
        promo.promo_unique = promos
    else:
        promo.promo_common = schema.promo_common

    session.add(promo)
    session.commit()
    session.refresh(promo)

    return promo
