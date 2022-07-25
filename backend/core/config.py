import os
from pathlib import Path

from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path = env_path)


class Settings:
    PROJECT_NAME: str = "My Hero API"
    PROJECT_VERSION: str = "0.1.0"

    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    DATABASE_URL = os.getenv("")
    DETA_USER: str = os.getenv("DETA_USER")
    DETA_PASSWORD: os.getenv("DETA_PASSWORD")
    SECRET_KEY: os.getenv("SECRET_KEY")
    TEST_USER_EMAIL = "test@example.com"

settings = Settings()


