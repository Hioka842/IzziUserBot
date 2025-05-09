from telethon import TelegramClient, events
import logging
import os
import importlib.util
import asyncio
import pyfiglet
from datetime import datetime

# Конфигурация
API_ID = 
API_HASH = ""
BOT_TOKEN = " "
# 
# Настройка логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация клиента
client = TelegramClient('izziUser', API_ID, API_HASH)

def show_welcome():
    """Показывает фиолетовый ASCII-арт при запуске"""
    purple = "\033[95m"
    reset = "\033[0m"
    
    ascii_art = pyfiglet.figlet_format("IzziBot", font="slant")
    print(f"{purple}{ascii_art}{reset}")
    print(f"{purple}╔════════════════════════════╗")
    print(f"{purple}║{' '*28}║")
    print(f"{purple}║   Version: 1.0{' '*12}║")
    print(f"{purple}║   Developer: @pythongoha{' '*5}║")
    print(f"{purple}║   Launch: {datetime.now().strftime('%d.%m.%Y %H:%M')}{' '*3}║")
    print(f"{purple}║{' '*28}║")
    print(f"{purple}╚════════════════════════════╝{reset}\n")

# Создаем папку modules если её нет
if not os.path.exists('modules'):
    os.makedirs('modules')

async def load_modules():
    """Загружает все модули из папки modules при старте"""
    loaded_count = 0
    for filename in os.listdir('modules'):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            try:
                spec = importlib.util.spec_from_file_location(
                    module_name, 
                    f"modules/{filename}"
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'register'):
                    module.register(client)
                    loaded_count += 1
                    logger.info(f"✅ Модуль {module_name} загружен")
            except Exception as e:
                logger.error(f"❌ Ошибка загрузки модуля {module_name}: {e}")
    return loaded_count

@client.on(events.NewMessage(pattern=r'\.rek$'))
async def rek_handler(event):
    try:
        await event.edit(
            "🗡️ <b>Лучший игровой бот в Telegram</b>\n"
            "@pythongoha\n"
            "@piar_izzi",
            parse_mode='html'
        )
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await event.reply("⚠️ Не удалось отредактировать сообщение")

@client.on(events.NewMessage(pattern=r'\.dlmod$'))
async def dlmod_handler(event):
    if not event.is_reply:
        await event.edit("❌ Ответьте на файл модуля!")
        return

    replied = await event.get_reply_message()
    
    if not replied.document:
        await event.edit("❌ Нужен файл .py!")
        return

    if not replied.file.name.endswith('.py'):
        await event.edit("❌ Только .py файлы!")
        return

    module_path = f"modules/{replied.file.name}"
    
    try:
        await replied.download_media(module_path)
        module_name = replied.file.name[:-3]
        spec = importlib.util.spec_from_file_location(
            module_name,
            module_path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, 'register'):
            module.register(client)
            await event.edit(f"✅ Модуль {replied.file.name} установлен и сохранен!")
        else:
            os.remove(module_path)
            await event.edit("❌ Нет функции register() в модуле!")
    except Exception as e:
        if os.path.exists(module_path):
            os.remove(module_path)
        await event.edit(f"❌ Ошибка: {str(e)}")

async def main():
    show_welcome()
    await client.start()
    
    purple = "\033[95m"
    reset = "\033[0m"
    
    logger.info("Загружаем модули...")
    loaded = await load_modules()
    print(f"{purple}✦ Modules loaded: {loaded}{reset}")
    
    logger.info("Юзербот запущен!")
    print(f"{purple}╔════════════════════════════╗")
    print(f"{purple}║    IzziBot успешно запущен!{' '*3}║")
    print(f"{purple}╚════════════════════════════╝{reset}")
    
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}")
