import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Travel Planner API"
    VERSION: str = "1.0.0"
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "").split(",")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./travel_planner.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    GIGA_CERT_PATH: str = os.getenv("GIGA_CERT_PATH", "./russian_trusted_root_ca_pem.crt")
    GIGA_AUTH_TOKEN: str = os.getenv("GIGA_AUTH_TOKEN", "YmZlNGMwYWQtM2E0ZS00NzQ3LWIzMzQtZWYxN2NjNTYxODEyOmZjOWQ0ZDNlLTlhMzctNGRiMi1iNTVmLTMzMjYwNmI2MzBjZg==")
settings = Settings()