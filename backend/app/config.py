from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    gemini_api_key: str
    database_url: str = "sqlite:///./finance.db"
    timezone: str = "America/Vancouver"
    enable_scheduler: bool = False  


settings = Settings()