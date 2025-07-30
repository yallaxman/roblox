import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from nickname_generator import NicknameGenerator
from config import TELEGRAM_BOT_TOKEN

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация генератора никнеймов
nickname_gen = NicknameGenerator()

# Словарь для хранения состояния пользователей
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_message = """
🎮 *Добро пожаловать в Roblox Nickname Generator!*

Я помогу тебе создать крутые никнеймы для Roblox! 

Доступные команды:
• /generate - Сгенерировать случайные никнеймы
• /custom - Создать никнейм по твоим предпочтениям
• /styles - Показать доступные стили
• /help - Показать справку

Выбери команду или нажми кнопку ниже!
    """
    
    keyboard = [
        [InlineKeyboardButton("🎲 Случайные никнеймы", callback_data="generate_random")],
        [InlineKeyboardButton("🎨 Кастомные никнеймы", callback_data="custom_nickname")],
        [InlineKeyboardButton("📋 Доступные стили", callback_data="show_styles")],
        [InlineKeyboardButton("❓ Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, parse_mode='Markdown', reply_markup=reply_markup)

async def generate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /generate"""
    await generate_random_nicknames(update, context)

async def generate_random_nicknames(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Генерирует случайные никнеймы"""
    user_id = update.effective_user.id
    
    # Отправляем сообщение о загрузке
    loading_message = await update.message.reply_text("🔄 Генерирую никнеймы...")
    
    try:
        # Генерируем никнеймы
        nicknames = nickname_gen.generate_nickname()
        
        if nicknames and nicknames[0] not in ["ErrorGenerating", "ErrorParsing"]:
            response = "🎮 *Сгенерированные никнеймы для Roblox:*\n\n"
            for i, nickname in enumerate(nicknames, 1):
                response += f"{i}. `{nickname}`\n"
            
            response += "\n💡 *Советы:*\n"
            response += "• Скопируй никнейм и проверь его доступность в Roblox\n"
            response += "• Попробуй добавить цифры, если никнейм занят\n"
            response += "• Используй /custom для создания никнейма по твоим предпочтениям"
            
            # Создаем кнопки для быстрого доступа
            keyboard = [
                [InlineKeyboardButton("🔄 Еще никнеймы", callback_data="generate_random")],
                [InlineKeyboardButton("🎨 Кастомные", callback_data="custom_nickname")],
                [InlineKeyboardButton("📋 Стили", callback_data="show_styles")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await loading_message.edit_text(response, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            await loading_message.edit_text("❌ Ошибка при генерации никнеймов. Попробуй позже!")
            
    except Exception as e:
        logger.error(f"Ошибка при генерации никнеймов: {e}")
        await loading_message.edit_text("❌ Произошла ошибка. Попробуй позже!")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /custom"""
    user_id = update.effective_user.id
    user_states[user_id] = "waiting_for_preference"
    
    message = """
🎨 *Создание кастомного никнейма*

Опиши, какой никнейм ты хочешь! Например:
• "Крутой и страшный"
• "Милый и розовый"
• "Космический воин"
• "Аниме персонаж"
• "Киберпанк стиль"

Просто напиши свои предпочтения в следующем сообщении!
    """
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def handle_custom_preference(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает пользовательские предпочтения для кастомных никнеймов"""
    user_id = update.effective_user.id
    
    if user_id in user_states and user_states[user_id] == "waiting_for_preference":
        preference = update.message.text
        
        # Удаляем состояние пользователя
        del user_states[user_id]
        
        # Отправляем сообщение о загрузке
        loading_message = await update.message.reply_text("🎨 Создаю кастомные никнеймы...")
        
        try:
            # Генерируем кастомные никнеймы
            nicknames = nickname_gen.generate_custom_nickname(preference)
            
            if nicknames and nicknames[0] not in ["CustomError"]:
                response = f"🎨 *Кастомные никнеймы на основе:* `{preference}`\n\n"
                for i, nickname in enumerate(nicknames, 1):
                    response += f"{i}. `{nickname}`\n"
                
                response += "\n💡 *Советы:*\n"
                response += "• Проверь доступность никнейма в Roblox\n"
                response += "• Попробуй /generate для случайных вариантов\n"
                
                keyboard = [
                    [InlineKeyboardButton("🔄 Еще кастомные", callback_data="custom_nickname")],
                    [InlineKeyboardButton("🎲 Случайные", callback_data="generate_random")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await loading_message.edit_text(response, parse_mode='Markdown', reply_markup=reply_markup)
            else:
                await loading_message.edit_text("❌ Ошибка при создании кастомных никнеймов. Попробуй позже!")
                
        except Exception as e:
            logger.error(f"Ошибка при создании кастомных никнеймов: {e}")
            await loading_message.edit_text("❌ Произошла ошибка. Попробуй позже!")

async def styles_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /styles"""
    await show_styles(update, context)

async def show_styles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает доступные стили никнеймов"""
    styles_message = """
📋 *Доступные стили никнеймов:*

🎮 **Игровые стили:**
• Крутые и агрессивные
• Милые и кавайные
• Киберпанк и футуристические
• Фэнтези и магические
• Космические и галактические

🎨 **Темы:**
• Аниме персонажи
• Супергерои
• Викинги и воины
• Космонавты и пилоты
• Маги и волшебники
• Роботы и андроиды

💡 *Используй команду /custom чтобы создать никнейм в любом стиле!*
    """
    
    keyboard = [
        [InlineKeyboardButton("🎲 Случайные никнеймы", callback_data="generate_random")],
        [InlineKeyboardButton("🎨 Кастомные никнеймы", callback_data="custom_nickname")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(styles_message, parse_mode='Markdown', reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await show_help(update, context)

async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает справку"""
    help_message = """
❓ *Справка по использованию бота*

🎮 **Основные команды:**
• `/start` - Главное меню
• `/generate` - Сгенерировать случайные никнеймы
• `/custom` - Создать кастомный никнейм
• `/styles` - Показать доступные стили
• `/help` - Эта справка

💡 **Как использовать:**
1. Выбери команду или нажми кнопку
2. Для кастомных никнеймов опиши свои предпочтения
3. Скопируй понравившийся никнейм
4. Проверь его доступность в Roblox

⚠️ **Важно:**
• Никнеймы генерируются с помощью ИИ
• Всегда проверяй доступность в Roblox
• Используй только буквы, цифры и подчеркивания
• Длина никнейма: 3-20 символов

🆘 **Если что-то не работает:**
Попробуй перезапустить бота командой /start
    """
    
    keyboard = [
        [InlineKeyboardButton("🏠 Главное меню", callback_data="start")],
        [InlineKeyboardButton("🎲 Случайные никнеймы", callback_data="generate_random")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(help_message, parse_mode='Markdown', reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "generate_random":
        # Создаем фейковое сообщение для генерации
        fake_message = type('obj', (object,), {
            'reply_text': lambda text, **kwargs: query.edit_message_text(text, **kwargs),
            'message': query.message,
            'effective_user': query.from_user
        })()
        await generate_random_nicknames(fake_message, context)
        
    elif query.data == "custom_nickname":
        user_id = query.from_user.id
        user_states[user_id] = "waiting_for_preference"
        
        message = """
🎨 *Создание кастомного никнейма*

Опиши, какой никнейм ты хочешь! Например:
• "Крутой и страшный"
• "Милый и розовый"
• "Космический воин"
• "Аниме персонаж"
• "Киберпанк стиль"

Просто напиши свои предпочтения в следующем сообщении!
        """
        
        keyboard = [
            [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)
        
    elif query.data == "show_styles":
        await show_styles(query, context)
        
    elif query.data == "help":
        await show_help(query, context)
        
    elif query.data == "start":
        await start(query, context)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Ошибка при обработке обновления {update}: {context.error}")

def main():
    """Основная функция запуска бота"""
    # Создаем приложение
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("generate", generate_command))
    application.add_handler(CommandHandler("custom", custom_command))
    application.add_handler(CommandHandler("styles", styles_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Добавляем обработчики кнопок
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Добавляем обработчик текстовых сообщений для кастомных никнеймов
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_preference))
    
    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("🤖 Бот запущен! Нажми Ctrl+C для остановки.")
    application.run_polling()

if __name__ == '__main__':
    main()