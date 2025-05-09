#!/bin/bash
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo -e "${YELLOW}🚀 Начинаем установку IzziUserBot...${NC}"

# 1. Фиксируем репозитории Termux
echo -e "${GREEN}✅ Настраиваем репозитории Termux...${NC}"
termux-change-repo <<< $'1\n1\n'

# 2. Устанавливаем базовые пакеты
echo -e "${GREEN}✅ Устанавливаем Python и Git...${NC}"
pkg update -y && pkg install -y python git wget

# 3. Устанавливаем pip и зависимости
echo -e "${GREEN}✅ Устанавливаем Telethon...${NC}"
python -m ensurepip --upgrade
python -m pip install --upgrade pip telethon

# 4. Скачиваем бота через wget (если git не работает)
echo -e "${GREEN}✅ Загружаем IzziUserBot...${NC}"
wget https://github.com/Hioka842/IzziUserBot/archive/main.zip -O IzziBot.zip
unzip IzziBot.zip -d ~/
mv ~/IzziUserBot-main ~/IzziUserBot
cd ~/IzziUserBot

# 5. Настройка конфига
echo -e "${YELLOW}🔧 Введите данные от Telegram:${NC}"
read -p "API_ID: " api_id
read -p "API_HASH: " api_hash
read -p "Номер телефона: " phone

echo "API_ID = $api_id
API_HASH = '$api_hash'
PHONE = '$phone'" > config.py

# 6. Запуск
echo -e "${GREEN}✅ Запускаем бота...${NC}"
python IzziBot.py &
