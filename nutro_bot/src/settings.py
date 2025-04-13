import logging
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_token: str
    log_level: str = "INFO"  # Default log level

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