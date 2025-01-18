from src.api.schemas import Email, Password


class BusinessCreate(Email, Password):
    name: str
