#!/bin/bash

# Ranglar
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     📚 DAVOMAT TIZIMI - TO'LIQ ISHGA TUSHIRISH          ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Loyiha papkasi
cd /Users/artursettarov/project/tatu_site

# Virtual muhitni faollashtirish
source venv/bin/activate

echo -e "${YELLOW}[1/5] PostgreSQL tekshirilmoqda...${NC}"
if pg_isready -q; then
    echo -e "${GREEN}✅ PostgreSQL ishlayapti${NC}"
else
    echo -e "${RED}❌ PostgreSQL ishlamayapti! Iltimos, PostgreSQL ni ishga tushiring.${NC}"
    exit 1
fi

echo -e "${YELLOW}[2/5] Redis tekshirilmoqda...${NC}"
if redis-cli ping 2>/dev/null | grep -q "PONG"; then
    echo -e "${GREEN}✅ Redis ishlayapti${NC}"
else
    echo -e "${YELLOW}⚠️ Redis ishlamayapti, ishga tushirilmoqda...${NC}"
    redis-server --daemonize yes
    sleep 2
    echo -e "${GREEN}✅ Redis ishga tushdi${NC}"
fi

echo -e "${YELLOW}[3/5] Migratsiyalar tekshirilmoqda...${NC}"
python manage.py migrate --noinput > /dev/null 2>&1
echo -e "${GREEN}✅ Migratsiyalar tayyor${NC}"

echo -e "${YELLOW}[4/5] Django server ishga tushirilmoqda...${NC}"
python manage.py runserver 8000 > /dev/null 2>&1 &
DJANGO_PID=$!
sleep 3
echo -e "${GREEN}✅ Django server ishga tushdi (PID: $DJANGO_PID)${NC}"

echo -e "${YELLOW}[5/5] Celery va Bot ishga tushirilmoqda...${NC}"
celery -A config worker --loglevel=info --pool=solo > celery.log 2>&1 &
CELERY_PID=$!
sleep 2

python apps/notifications/bot.py > bot.log 2>&1 &
BOT_PID=$!
sleep 2

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     ✅ HAMMA TIZIMLAR ISHGA TUSHIRILDI!                  ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📊 ADMIN PANEL:${NC}    http://127.0.0.1:8000/admin"
echo -e "${BLUE}📱 TELEGRAM BOT:${NC}   @davomat_bot"
echo ""
echo -e "${YELLOW}📝 Log fayllar:${NC}"
echo "   - celery.log  (Celery xatolari)"
echo "   - bot.log     (Bot xatolari)"
echo ""
echo -e "${RED}⛔ To'xtatish uchun:${NC} ./stop_all.sh"
echo ""

# PID larni saqlash
echo "$DJANGO_PID" > .pids
echo "$CELERY_PID" >> .pids
echo "$BOT_PID" >> .pids

# Loglarni kuzatish
tail -f bot.log celery.log 2>/dev/null