from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Configuration
    api_key: str
    api_secret: str
    oauth_url: str
    authorization_header: str
    rquid: str

    # Payload Configuration
    scope: str
    gigachat_scope: str = "GIGACHAT_API_PERS"
    gigachat_model: str = 'GigaChat'
    log_level: str = "INFO"
    debug_mode: bool = False
    verify_ssl_certs: bool = False

    @property
    def gigachat_credentials(self) -> str:
        # Use the API_KEY directly as the credentials
        return self.api_key

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()