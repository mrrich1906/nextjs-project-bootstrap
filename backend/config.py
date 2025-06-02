from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    # WhatsApp API Configuration
    WHATSAPP_API_TOKEN: str
    WHATSAPP_API_URL: str
    WHATSAPP_VERIFY_TOKEN: str
    
    # Google Sheets Configuration
    GOOGLE_SHEETS_CREDENTIALS: str
    GOOGLE_SHEETS_SPREADSHEET_ID: str
    
    # Admin Configuration
    ADMIN_PHONE_NUMBERS: list[str]
    
    # Optional Payment Gateway Configuration
    PAYMENT_GATEWAY_ENABLED: bool = False
    PAYMENT_GATEWAY_API_KEY: Optional[str] = None
    PAYMENT_GATEWAY_SECRET: Optional[str] = None
    
    # Backup Configuration
    BACKUP_ENABLED: bool = True
    BACKUP_EMAIL: Optional[str] = None
    BACKUP_FREQUENCY_HOURS: int = 24
    
    # Room Configuration
    AVAILABLE_ROOMS: list[str]
    ROOM_PRICES: dict[str, float]
    
    # Application Configuration
    DEBUG: bool = False
    PORT: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
