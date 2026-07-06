"""Environment configuration loaded from .env file."""

import os

from dotenv import load_dotenv

load_dotenv()


class Environment:
    base_url: str = os.getenv("BASE_URL", "http://localhost:3000")
    api_url: str = os.getenv("API_URL", os.getenv("BASE_URL", "http://localhost:3000"))
