from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    gemini_api_key: str
    database_url: str = "sqlite:///./finance.db"
    timezone: str = "America/Vancouver"
    enable_scheduler: bool = False  
    admin_token: str = "changeme"          # ← 新增:admin 密钥,默认值随便,真实值放 .env/Railway


settings = Settings()