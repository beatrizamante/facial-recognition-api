"This is the .env decrypt configuration module"

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv
from typing import Union
import base64

load_dotenv()

class Setting(BaseSettings):
    DB_USER=
    DB_PASSWORD=
    DB_HOST=
    DB_PORT=
    DB_DATABASE=
    BASE_MICROSOFT_URL="https://graph.microsoft,com/v1.0"

    config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
