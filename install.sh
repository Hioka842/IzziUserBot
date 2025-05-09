#!/bin/bash
# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Проверка Termux
if [ ! -d "$PREFIX" ]; then
    echo -e "${RED}❌ Ошибка: Этот скрипт работает только в Termux!${NC}"
    exit 1
fi

echo -e "${CYAN}_______________________________________________________${NC}"
echo -e "${YELLOW}🚀 Начинаем установку IzziUserBot...${NC}"
echo -e "${CYAN}_______________________________________________________${NC}"

# Установка зависимостей
echo -e "${GREEN}✅ Обновляем пакеты и устанавливаем Python/Git...${NC}"
pkg update -y && pkg install -y python git wget

# Установка библиотек
echo -e "${GREEN}✅ Устанавливаем Telethon...${NC}"
pip install --upgrade pip && pip install telethon

# Скачивание бота
echo -e "${GREEN}✅ Клонируем репозиторий...${NC}"
git clone https://github.com/Hioka842/IzziUserBot.git ~/IzziUserBot
cd ~/IzziUserBot

# Проверка файлов
if [ ! -f "IzziBot.py" ]; then
    echo -e "${RED}❌ Ошибка: Файл IzziBot.py не найден в репозитории!${NC}"
    exit 1
fi

# Настройка конфига
echo -e "${CYAN}_______________________________________________________${NC}"
echo -e "${YELLOW}🔧 Введите данные от Telegram аккаунта:${NC}"
echo -e "${CYAN}_______________________________________________________${NC}"

read -p "API_ID (получить на my.telegram.org): " api_id
read -p "API_HASH: " api_hash
read -p "Номер телефона (с кодом страны): " phone

echo "API_ID = $api_id
API_HASH = '$api_hash'
PHONE = '$phone'" > config.py

# Установка прав
chmod +x IzziBot.py

# Запуск
echo -e "${GREEN}✅ Запускаем бота в фоне...${NC}"
nohup python IzziBot.py > bot.log 2>&1 &

echo -e "${CYAN}_______________________________________________________${NC}"
echo -e "${YELLOW}✨ Установка успешно завершена!${NC}"
echo -e "${CYAN}_______________________________________________________${NC}"
echo -e "${GREEN}▪ Бот запущен в фоновом режиме${NC}"
echo -e "${GREEN}▪ Логи: ${CYAN}tail -f ~/IzziUserBot/bot.log${NC}"
echo -e "${GREEN}▪ Остановка: ${RED}pkill -f IzziBot.py${NC}"
echo -e "${GREEN}▪ Ручной запуск: ${CYAN}cd ~/IzziUserBot && python IzziBot.py${NC}"
echo -e "${CYAN}_______________________________________________________${NC}"
