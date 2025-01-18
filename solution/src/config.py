import typing

from pydantic import DirectoryPath, NewPath, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

GeneratedPath = NewPath | DirectoryPath


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    JWT_EXPIRE_MINUTES: int = 1440

    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_HOST: str
    POSTGRES_DATABASE: str

    REDIS_HOST: str
    REDIS_PORT: int

    @computed_field
    @property
    def POSTGRES_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USERNAME,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DATABASE,
        )

    SWAGGER_UI_PARAMETERS: dict[typing.Any, typing.Any] = {
        "persistAuthorization": True,
    }

    # def model_post_init(self, _: typing.Any) -> None:
    #     attrs = self.__annotations__.items()
    #     generated_path_attrs = (attr for attr, attr_type in attrs if attr_type == GeneratedPath)
    #     for attr in generated_path_attrs:
    #         pathname = getattr(self, attr)
    #         os.makedirs(pathname, exist_ok=True)


settings = Settings()
