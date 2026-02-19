from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    USER_DB: str
    PASSWORD_DB: str
    HOST_DB: str
    PORT_DB: str
    DATABASE: str
    SECRET_KEY: str
    ALGORITHM: str
    EMAIL_TEST_USER: str | None = None
    PASSWORD_TEST_USER: str | None = None
    JWT_ISSUER: str
    JWT_AUDIENCE: str
    URL_API_OS: str
    MP_ACCESS_TOKEN: str
    MP_API: str
    MP_SUCCESS_URL: str
    MP_FAILURE_URL: str
    MP_PENDING_URL: str
    MP_NOTIFICATION_URL: str


settings = Settings()  # type: ignore
