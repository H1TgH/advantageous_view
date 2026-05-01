from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


BaseSettings.model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="allow",
)


class DataBaseSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: SecretStr
    db: str

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"

    model_config = SettingsConfigDict(env_prefix="POSTGRES_")


class SecuritySettings(BaseSettings):
    secret_key: SecretStr
    algorithm: str
    access_ttl: int = Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_ttl: int = Field(alias="REFRESH_TOKEN_EXPIRE_DAYS")


class SMTPSettings(BaseSettings):
    host: str = "smtp.gmail.com"
    port: int = 465
    user: str = ""
    password: SecretStr = SecretStr("")
    from_email: str = ""

    model_config = SettingsConfigDict(env_prefix="SMTP_")


class RedisSettings(BaseSettings):
    host: str = "redis"
    port: int = 6379

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/0"

    model_config = SettingsConfigDict(env_prefix="REDIS_")


class Settings(BaseSettings):
    db: DataBaseSettings = Field(default_factory=DataBaseSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    smtp: SMTPSettings = Field(default_factory=SMTPSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    apisystem_key: str = Field(alias="APISYSTEM_KEY")


settings = Settings()
