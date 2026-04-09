import logging
from celery import shared_task
from django.conf import settings
from telegram import Bot

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def telegram_xabar_yubor(self, chat_id, matn, sarlavha, tur):
    """Telegram orqali xabar yuborish"""
    try:
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        
        # Xabarni formatlash
        belgi = {
            'WARNING': '⚠️',
            'ALERT': '🔴',
            'REPORT': '📊'
        }.get(tur, '📢')
        
        toliq_matn = f"{belgi} *{sarlavha}*\n\n{matn}\n\n---\nDavomat Tizimi"
        
        bot.send_message(
            chat_id=chat_id,
            text=toliq_matn,
            parse_mode='Markdown'
        )
        
        logger.info(f"Telegram xabar yuborildi: {chat_id}")
        return {'status': 'success', 'chat_id': chat_id}
        
    except Exception as e:
        logger.error(f"Telegram xabar yuborishda xato: {e}")
        self.retry(exc=e, countdown=60)