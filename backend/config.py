import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Settings:
    razorpay_key_id = os.getenv("RAZORPAY_KEY_ID", "")
    razorpay_key_secret = os.getenv("RAZORPAY_KEY_SECRET", "")
    groq_api_key = os.getenv("GROQ_API_KEY", "")
    database_url = os.getenv("DATABASE_URL", "sqlite:///./merchant.db")
    daily_limit_paise = int(os.getenv("DAILY_LIMIT_PER_AGENT", "5000"))

    @property
    def database_path(self) -> str:
        if self.database_url.startswith("sqlite:///"):
            path = self.database_url.removeprefix("sqlite:///")
        else:
            path = self.database_url
        return str(Path(path))


settings = Settings()