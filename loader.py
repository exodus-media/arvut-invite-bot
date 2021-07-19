from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram import types

from data.config import I18N_DOMAIN, LOCALES_DIR
from data import config
from language_middleware import setup_middleware

bot = Bot(token=str(config.BOT_TOKEN), parse_mode=types.ParseMode.HTML)
# storage = MemoryStorage()
storage = RedisStorage2(host='localhost', port=6379, db=5)

dp = Dispatcher(bot, storage=storage)


i18n = setup_middleware(dp)
# Создадим псевдоним для метода gettext
_ = i18n.gettext