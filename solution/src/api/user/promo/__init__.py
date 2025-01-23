from src.api.user.promo.comments import comments_router
from src.api.user.promo.routes import promo_router

promo_router.include_router(comments_router)

__all__ = [
    "promo_router",
]
