import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Настройки Telegram бота
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Настройки OpenRouter API
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'anthropic/claude-3.5-sonnet')

# Проверяем, что все необходимые переменные установлены
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен в переменных окружения")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY не установлен в переменных окружения")