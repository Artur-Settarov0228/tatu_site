import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from django.conf import settings
from apps.users.models import Foydalanuvchi

logger = logging.getLogger(__name__)

class DavomatBot:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        try:
            db_user = Foydalanuvchi.objects.get(telegram_chat_id=str(user.id))
            if db_user.roli == 'OTA_ONA':
                await update.message.reply_text(f"👋 Assalomu alaykum {db_user.get_full_name()}!\n\n📊 /stats - Statistika\n📅 /davomat - Darslar tarixi")
                return
        except Foydalanuvchi.DoesNotExist:
            pass
        
        tugma = [[KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True)]]
        await update.message.reply_text("👋 Xush kelibsiz! Telefon raqamingizni yuboring:", reply_markup=ReplyKeyboardMarkup(tugma, one_time_keyboard=True, resize_keyboard=True))
    
    async def telefon_olish(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        contact = update.message.contact
        telefon = contact.phone_number
        if not telefon.startswith('+'):
            telefon = f"+{telefon}" if telefon.startswith('998') else f"+998{telefon}"
        
        try:
            user = Foydalanuvchi.objects.get(telefon=telefon, roli='OTA_ONA')
            user.telegram_chat_id = str(update.effective_user.id)
            user.tasdiqlangan = True
            user.save()
            await update.message.reply_text(f"✅ Tasdiqlandi! Xush kelibsiz {user.get_full_name()}!\n\n/stats - Statistika\n/davomat - Davomat")
        except Foydalanuvchi.DoesNotExist:
            await update.message.reply_text("❌ Telefon raqam topilmadi!")
    
    async def statistika(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            user = Foydalanuvchi.objects.get(telegram_chat_id=str(update.effective_user.id))
            ota_ona = user.ota_ona_profili
            matn = "📊 *Statistika*\n\n"
            for talaba in ota_ona.talabalar.all():
                matn += f"*{talaba.toliq_ism}*\n❌ NB: {talaba.nb_soni}\n📉 Ketma-ket: {talaba.ketma_ket_nb_olish()}\n\n"
            await update.message.reply_text(matn, parse_mode='Markdown')
        except:
            await update.message.reply_text("/start bosing")
    
    async def davomat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            user = Foydalanuvchi.objects.get(telegram_chat_id=str(update.effective_user.id))
            ota_ona = user.ota_ona_profili
            matn = "📅 *Oxirgi darslar*\n\n"
            for talaba in ota_ona.talabalar.all():
                matn += f"*{talaba.toliq_ism}*\n"
                for d in talaba.davomatlar.order_by('-sana')[:5]:
                    holat = "✅" if d.holat == 'KELDI' else "❌"
                    matn += f"{holat} {d.sana}: {d.fan.nomi}\n"
                matn += "\n"
            await update.message.reply_text(matn, parse_mode='Markdown')
        except:
            await update.message.reply_text("/start bosing")
    
    async def xato(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("❓ Tushunarsiz buyruq.\n/stats - Statistika\n/davomat - Davomat")
    
    def run(self):
        if not self.token:
            print("❌ Bot token topilmadi!")
            return
        app = Application.builder().token(self.token).build()
        app.add_handler(CommandHandler('start', self.start))
        app.add_handler(CommandHandler('stats', self.statistika))
        app.add_handler(CommandHandler('davomat', self.davomat))
        app.add_handler(MessageHandler(filters.CONTACT, self.telefon_olish))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.xato))
        print("🚀 Bot ishga tushdi...")
        app.run_polling()

if __name__ == '__main__':
    DavomatBot().run()