import logging
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Configuration
    gigachat_credentials: str
    gigachat_scope: str = "GIGACHAT_API_PERS"
    gigachat_model: str = 'GigaChat'
    log_level: str = "INFO"  # Default log level
    debug_mode: bool = False
    verify_ssl_certs: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def configure_logging(self):
        """
        Configures the logging settings based on the log_level.
        """
        logging.basicConfig(
            level=getattr(logging, self.log_level.upper(), logging.INFO),
            format="%(asctime)s - %(levelname)s - %(message)s",
        )


# Initialize settings and configure logging
settings = Settings()
settings.configure_logging()