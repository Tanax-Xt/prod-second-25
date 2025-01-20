from pydantic import DirectoryPath, NewPath, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

GeneratedPath = NewPath | DirectoryPath


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    JWT_EXPIRE_MINUTES: int = 1440
    JWT_ALGORITHM: str = "HS256"

    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_HOST: str
    POSTGRES_DATABASE: str

    REDIS_HOST: str
    REDIS_PORT: int

    BUSINESS_SECRET_PREFIX: str = "b-secret"
    USER_SECRET_PREFIX: str = "u-secret"

    @computed_field
    @property
    def POSTGRES_URI(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USERNAME,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DATABASE,
        )


settings = Settings()
