from pydantic import BaseSettings


class Settings(BaseSettings):
    gigachat_credentials: str = "default_credentials"
    gigachat_scope: str = "GIGACHAT_API_PERS"
    gigachat_model: str = "GigaChat Lite"
    verify_ssl_certs: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()