#!/usr/bin/env python
import os
import sys
import django

# Django settings ni sozlash (MUHIM!)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from django.conf import settings
from apps.users.models import Foydalanuvchi, OtaOna

logger = logging.getLogger(__name__)

class DavomatBot:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """1. /start buyrug'i - telefon raqam so'rash"""
        user_id = str(update.effective_user.id)
        
        # Foydalanuvchi allaqachon ro'yxatdan o'tganmi?
        try:
            user = Foydalanuvchi.objects.get(telegram_chat_id=user_id)
            if user.roli == 'OTA_ONA':
                await update.message.reply_text(
                    f"👋 Assalomu alaykum {user.get_full_name()}!\n\n"
                    f"✅ Siz allaqachon ro'yxatdan o'tgansiz.\n\n"
                    f"📊 /stats - Statistika ko'rish\n"
                    f"📅 /davomat - Darslar tarixi"
                )
                return
        except Foydalanuvchi.DoesNotExist:
            pass
        
        # Yangi foydalanuvchi - telefon raqam so'rash
        button = [[KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(button, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            "👋 Xush kelibsiz! Iltimos, ro'yxatdan o'tish uchun telefon raqamingizni yuboring:",
            reply_markup=reply_markup
        )
    
    async def phone_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """2. Telefon raqamni qabul qilish va bazaga saqlash"""
        contact = update.message.contact
        if not contact:
            await update.message.reply_text("Iltimos, telefon raqam tugmasini bosing!")
            return
        
        telefon = contact.phone_number
        # Telefonni formatlash +998XXXXXXXXX
        if not telefon.startswith('+'):
            if telefon.startswith('998'):
                telefon = f"+{telefon}"
            else:
                telefon = f"+998{telefon}"
        
        # Bazada telefon raqamni qidirish
        try:
            user = Foydalanuvchi.objects.get(telefon=telefon, roli='OTA_ONA')
            
            # Telegram chat ID ni saqlash
            user.telegram_chat_id = str(update.effective_user.id)
            user.tasdiqlangan = True
            user.save()
            
            # Xabar: Telefon raqam saqlandi!
            await update.message.reply_text(
                f"✅ Telefon raqamingiz saqlandi!\n\n"
                f"👋 Xush kelibsiz {user.get_full_name()}!\n\n"
                f"Endi quyidagi buyruqlardan foydalanishingiz mumkin:\n"
                f"📊 /stats - Statistika ko'rish\n"
                f"📅 /davomat - Darslar tarixi"
            )
            
        except Foydalanuvchi.DoesNotExist:
            await update.message.reply_text(
                "❌ Kechirasiz, bu telefon raqam tizimda topilmadi.\n\n"
                "Iltimos, ro'yxatdan o'tish uchun maktabga murojaat qiling.\n"
                "Yoki to'g'ri telefon raqam yuborganingizga ishonch hosil qiling."
            )
    
    async def stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Statistika ko'rish"""
        try:
            user = Foydalanuvchi.objects.get(telegram_chat_id=str(update.effective_user.id))
            if user.roli != 'OTA_ONA':
                await update.message.reply_text("❌ Siz ota-ona emassiz!")
                return
            
            ota_ona = user.ota_ona_profili
            talabalar = ota_ona.talabalar.all()
            
            if not talabalar:
                await update.message.reply_text("📭 Sizga biriktirilgan farzand yo'q!")
                return
            
            matn = "📊 *FARZANDLARINGIZ STATISTIKASI*\n\n"
            for talaba in talabalar:
                nb_soni = talaba.nb_soni
                
                # Xavf darajasi
                if nb_soni >= 5:
                    xavf = "🔴 JIDDIY XAVF"
                    tavsiya = "❗ Darhol chora ko'ring!"
                elif nb_soni >= 3:
                    xavf = "🟡 O'RTA XAVF"
                    tavsiya = "⚠️ Diqqat qiling!"
                else:
                    xavf = "🟢 PAST XAVF"
                    tavsiya = "✅ Yaxshi davomat"
                
                matn += f"*{talaba.toliq_ism}*\n"
                matn += f"🎓 Guruh: {talaba.guruh.nomi}\n"
                matn += f"❌ Dars qoldirishlar: *{nb_soni}* ta\n"
                matn += f"⚡ Holat: {xavf}\n"
                matn += f"💡 {tavsiya}\n\n"
            
            await update.message.reply_text(matn, parse_mode='Markdown')
            
        except Foydalanuvchi.DoesNotExist:
            await update.message.reply_text("❌ Iltimos, avval /start bosing va ro'yxatdan o'ting!")
    
    async def davomat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Oxirgi davomatlarni ko'rish"""
        try:
            user = Foydalanuvchi.objects.get(telegram_chat_id=str(update.effective_user.id))
            if user.roli != 'OTA_ONA':
                await update.message.reply_text("❌ Siz ota-ona emassiz!")
                return
            
            ota_ona = user.ota_ona_profili
            talabalar = ota_ona.talabalar.all()
            
            if not talabalar:
                await update.message.reply_text("📭 Sizga biriktirilgan farzand yo'q!")
                return
            
            matn = "📅 *OXIRGI 5 KUNLIK DAVOMAT*\n\n"
            for talaba in talabalar:
                matn += f"*{talaba.toliq_ism}*\n"
                oxirgi_davomatlar = talaba.davomatlar.order_by('-sana')[:5]
                
                if oxirgi_davomatlar:
                    for d in oxirgi_davomatlar:
                        if d.holat == 'KELDI':
                            holat = "✅ Keldi"
                        else:
                            sabablar = {
                                'SABABSIZ': '❌ Sababsiz qoldirgan',
                                'KASAL': '🤒 Kasal bo\'lgan',
                                'RUXSAT': '📝 Ruxsat bilan qoldirgan'
                            }
                            holat = sabablar.get(d.sabab, '❌ Kelmagan')
                        matn += f"• {d.sana}: {d.fan.nomi} - {holat}\n"
                else:
                    matn += "📭 Ma'lumot yo'q\n"
                matn += "\n"
            
            await update.message.reply_text(matn, parse_mode='Markdown')
            
        except Foydalanuvchi.DoesNotExist:
            await update.message.reply_text("❌ Iltimos, avval /start bosing va ro'yxatdan o'ting!")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Tushunarsiz buyruq"""
        await update.message.reply_text(
            "❓ Tushunarsiz buyruq.\n\n"
            "Quyidagi buyruqlardan foydalaning:\n"
            "/start - Boshlash va ro'yxatdan o'tish\n"
            "/stats - Statistika ko'rish\n"
            "/davomat - Davomat tarixi"
        )
    
    def run(self):
        if not self.token:
            print("❌ Telegram bot token topilmadi! .env faylini tekshiring.")
            return
        
        print("🚀 Telegram bot ishga tushmoqda...")
        app = Application.builder().token(self.token).build()
        
        # Handlerlar
        app.add_handler(CommandHandler('start', self.start))
        app.add_handler(CommandHandler('stats', self.stats))
        app.add_handler(CommandHandler('davomat', self.davomat))
        app.add_handler(MessageHandler(filters.CONTACT, self.phone_handler))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.error_handler))
        
        print("✅ Bot muvaffaqiyatli ishga tushdi!")
        print("📱 Telegram bot: @davomat_bot")
        app.run_polling()


if __name__ == '__main__':
    bot = DavomatBot()
    bot.run()