from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from pydantic_settings import BaseSettings
from supabase import Client, create_client

from src.repo.PupilDataRepo import PupilDataRepository
from src.repo.UserDataRepo import UserDataRepository


class Secrets(BaseSettings):
    token: str
    admin_id: int
    supabase_url: str
    supabase_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


secrets = Secrets()

# Инициализация подключения к базе данных Supabase
url: str = secrets.supabase_url
key: str = secrets.supabase_key

# Создание клиента Supabase
supabase: Client = create_client(url, key)

users_data_repo = UserDataRepository(supabase)
pupil_data_repo = PupilDataRepository(supabase)

# Инициализация бота
default = DefaultBotProperties(parse_mode='HTML', protect_content=False)
bot = Bot(token=secrets.token, default=default)
dp = Dispatcher()
