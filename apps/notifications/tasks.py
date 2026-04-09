import logging
from celery import shared_task
from django.conf import settings
from telegram import Bot

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_telegram_message(self, chat_id, message):
    """Telegram orqali xabar yuborish"""
    try:
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode='Markdown'
        )
        logger.info(f"✅ Xabar yuborildi! Chat ID: {chat_id}")
        return {'status': 'success', 'chat_id': chat_id}
        
    except Exception as e:
        logger.error(f"❌ Xatolik: {e}")
        # Qayta urinish
        self.retry(exc=e, countdown=60)