from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from pydantic_settings import BaseSettings
from supabase import Client, create_client


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

# Инициализация бота
default = DefaultBotProperties(parse_mode='HTML', protect_content=False)
bot = Bot(token=secrets.token, default=default)
dp = Dispatcher()
