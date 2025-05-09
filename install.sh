#!/bin/bash
# Цвета для красивого вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo -e "${YELLOW}🚀 Запуск установки IzziBot...${NC}"

# Установка зависимостей
echo -e "${GREEN}✅ Устанавливаем Python и Git...${NC}"
pkg update -y && pkg install -y python git

# Установка библиотек
echo -e "${GREEN}✅ Устанавливаем Telethon...${NC}"
pip install --upgrade pip telethon

# Скачивание бота
echo -e "${GREEN}✅ Клонируем репозиторий...${NC}"
git clone https://github.com/yourusername/IzziBot ~/IzziBot
cd ~/IzziBot

# Настройка конфига
echo -e "${YELLOW}🔧 Настройка конфигурации...${NC}"
read -p "Введите API_ID: " api_id
read -p "Введите API_HASH: " api_hash
read -p "Введите номер телефона: " phone

echo "API_ID = $api_id
API_HASH = '$api_hash'
PHONE = '$phone'" > config.py

# Запуск
echo -e "${GREEN}✅ Запускаем бота в фоне...${NC}"
python IzziBot.py &

echo -e "\n${YELLOW}✨ Установка завершена! Бот работает в фоне.${NC}"
echo -e "Для просмотра логов: ${GREEN}tail -f nohup.out${NC}"
echo -e "Для остановки: ${RED}pkill -f IzziBot.py${NC}"