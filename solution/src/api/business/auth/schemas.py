from src.api.schemas import Email, Password


class BusinessLogin(Email, Password):
    pass


class BusinessCreate(BusinessLogin):
    name: str
