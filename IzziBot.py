from telethon import TelegramClient, events
import logging
import os
import importlib
import asyncio
import pyfiglet
from datetime import datetime
import sys

# Настройка логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('izzi.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Проверка конфига
if not os.path.exists('config.py'):
    logger.error("❌ Файл config.py не найден! Сначала запустите install.sh")
    sys.exit(1)

# Инициализация клиента
try:
    from config import API_ID, API_HASH, PHONE
    client = TelegramClient('izziUser', API_ID, API_HASH)
except Exception as e:
    logger.error(f"❌ Ошибка загрузки конфига: {e}")
    sys.exit(1)

def show_welcome():
    """Показывает ASCII-арт при запуске"""
    purple = "\033[95m"
    reset = "\033[0m"
    
    ascii_art = pyfiglet.figlet_format("IzziBot", font="slant")
    print(f"{purple}{ascii_art}{reset}")
    print(f"{purple}╔════════════════════════════╗")
    print(f"{purple}║{' '*28}║")
    print(f"{purple}║   Version: 2.0{' '*12}║")
    print(f"{purple}║   Developer: @pythongoha{' '*5}║")
    print(f"{purple}║   Launch: {datetime.now().strftime('%d.%m.%Y %H:%M')}{' '*3}║")
    print(f"{purple}║{' '*28}║")
    print(f"{purple}╚════════════════════════════╝{reset}\n")

async def load_modules():
    """Загружает все модули из папки modules"""
    if not os.path.exists('modules'):
        os.makedirs('modules')
        return 0

    loaded_count = 0
    for filename in os.listdir('modules'):
        if not filename.endswith('.py') or filename.startswith('__'):
            continue
            
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
            logger.error(f"❌ Ошибка в модуле {module_name}: {str(e)}")
    
    return loaded_count

@client.on(events.NewMessage(pattern=r'\.rek$'))
async def rek_handler(event):
    """Пример команды"""
    try:
        await event.edit(
            "🗡️ <b>Лучший игровой бот в Telegram</b>\n"
            "@pythongoha\n"
            "@piar_izzi",
            parse_mode='html'
        )
    except Exception as e:
        logger.error(f"Ошибка: {e}")

@client.on(events.NewMessage(pattern=r'\.dlmod$'))
async def dlmod_handler(event):
    """Загрузка модулей"""
    if not event.is_reply:
        return await event.edit("❌ Ответьте на файл модуля!")

    replied = await event.get_reply_message()
    if not replied.document or not replied.file.name.endswith('.py'):
        return await event.edit("❌ Нужен .py файл!")
    
    module_path = f"modules/{replied.file.name}"
    try:
        await replied.download_media(module_path)
        module_name = replied.file.name[:-3]
        
        # Перезагружаем модуль
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, 'register'):
            module.register(client)
            await event.edit(f"✅ Модуль {replied.file.name} установлен!")
        else:
            os.remove(module_path)
            await event.edit("❌ Нет функции register() в модуле!")
            
    except Exception as e:
        if os.path.exists(module_path):
            os.remove(module_path)
        await event.edit(f"❌ Ошибка: {str(e)}")

@client.on(events.NewMessage(pattern=r'\.reload$'))
async def reload_handler(event):
    """Перезагрузка модулей"""
    if not event.out:
        return
    
    loaded = await load_modules()
    await event.edit(f"✅ Перезагружено модулей: {loaded}")

async def main():
    show_welcome()
    
    try:
        await client.start()
        logger.info("Юзербот авторизован")
        
        loaded = await load_modules()
        logger.info(f"Загружено модулей: {loaded}")
        
        print("\033[95m╔════════════════════════════╗")
        print("\033[95m║    IzziBot успешно запущен!    ║")
        print("\033[95m╚════════════════════════════╝\033[0m")
        
        await client.run_until_disconnected()
        
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
        sys.exit(0)
